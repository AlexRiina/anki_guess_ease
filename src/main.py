from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from anki.consts import CARD_TYPE_REV

LOG = logging.getLogger("guess_ease")


if TYPE_CHECKING:
    from anki.cards import Card


class Cache:
    """anki overwrites the factor on answering a new card, so I assign new
    cards to a variable before the ease is set and then after anki updates, I
    update again"""

    card: Optional[Card] = None


def reviewer_will_answer_card(ease_tuple, _, card: Card):
    if card.type < CARD_TYPE_REV:
        LOG.debug("%s: stored", card)
        Cache.card = card
    else:
        Cache.card = None

    return ease_tuple


def reviewer_did_answer_card(_, card: Card, ease):
    if Cache.card != card:
        LOG.debug("%s: not matched", card)

        return

    # must have gone from new/lrn -> rev, do we want this even with relearning?

    if card.type != CARD_TYPE_REV:
        LOG.debug("%s: skipping, not in review now")

        return

    # TODO probably want to skip the `ord` part of this query for cloze
    # deletions since {{c1::}} is hopefully not different from {{c2::}}

    note = card.note()
    assert note.col.db
    current_deck = note.col.decks.current()
    suggested_factor = note.col.db.scalar(
        "SELECT avg(cards.factor) "
        "FROM cards JOIN notes ON notes.id = cards.nid "
        "WHERE notes.mid = ? AND ivl > 21 AND ord = ? AND did = ?",
        note.mid,
        card.ord,
        current_deck["id"],
    )

    if suggested_factor:
        LOG.debug("%s: updating from %i -> %i", card, card.factor, suggested_factor)
        card.factor = int(suggested_factor)
        card.flush()
    else:
        LOG.debug("%s: no upgrade suggested", card, card.factor, suggested_factor)
