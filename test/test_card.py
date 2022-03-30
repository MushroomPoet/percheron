from test.cards import BLACK_LOTUS
from test.cards import TWINBLADE_GEIST
from test.cards import TWINBLADE_INVOCATION
from percheron.card import Card

def test_create():
    card = Card(BLACK_LOTUS)
    assert isinstance(card, Card)

def test_add_description():
    card = Card(TWINBLADE_GEIST)
    card.add_description(TWINBLADE_INVOCATION)
    assert len(card.descriptions) == 2

def test_value():
    card = Card(BLACK_LOTUS)
    assert card.value("convertedManaCost") == 0.0

def test_null_value():
    card = Card(BLACK_LOTUS)
    assert card.value("faceName") is None

def test_values():
    card = Card(TWINBLADE_GEIST)
    card.add_description(TWINBLADE_INVOCATION)
    values = card.values("types")
    assert ['Creature'] in values
    assert ['Enchantment'] in values

def test_has_value():
    card = Card(BLACK_LOTUS)
    assert card.has_value('convertedManaCost')
    assert not card.has_value('faceName')

def test_name():
    card = Card(BLACK_LOTUS)
    assert card.name() == "Black Lotus"

def test_no_float_draft_value():
    card = Card(BLACK_LOTUS)
    assert card.float_draft_value() == 0
