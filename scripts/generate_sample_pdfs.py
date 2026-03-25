"""Generate sample PDF poems for the Poetry RAG Critic knowledge base.

Run once:  python scripts/generate_sample_pdfs.py

Creates 12 placeholder "original" poems in data/my_poems/ and
6 public‑domain classic poems in data/public_poems/.
Requires: pip install fpdf2
"""

from pathlib import Path
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent
MY_DIR = BASE_DIR / "data" / "my_poems"
PUB_DIR = BASE_DIR / "data" / "public_poems"

# ── Original placeholder poems ─────────────────────────────────────────
MY_POEMS = {
    "morning_light.pdf": (
        "Morning Light\n\n"
        "The sun peels back the dark like skin from fruit,\n"
        "revealing gold that drips through windowpanes.\n"
        "I stand barefoot upon the kitchen tile\n"
        "and let the warmth remind me I am here.\n\n"
        "The kettle hums a low, forgiving note,\n"
        "steam curling upward like a question mark.\n"
        "Outside, the sparrows negotiate the hedge —\n"
        "small diplomats in coats of brown and grey.\n\n"
        "There is no urgency this early hour,\n"
        "only the slow persuasion of the day."
    ),
    "rust_and_memory.pdf": (
        "Rust and Memory\n\n"
        "The bicycle leans against the garden wall,\n"
        "its chain a bracelet of orange decay.\n"
        "No one has ridden it for seven years,\n"
        "yet no one thinks to throw the thing away.\n\n"
        "It holds its shape the way a word holds meaning\n"
        "long after you forget who said it first —\n"
        "a relic of some ordinary Tuesday\n"
        "when everything was neither best nor worst.\n\n"
        "I touch the handlebars.  They leave a stain\n"
        "of rust across my palm like bitter tea.\n"
        "Some things refuse to let you walk away\n"
        "without a mark to prove they used to be."
    ),
    "the_lighthouse_keeper.pdf": (
        "The Lighthouse Keeper\n\n"
        "He counts the seconds between flash and dark,\n"
        "a metronome of purpose on the cliff.\n"
        "The sea below churns phrases it can't finish,\n"
        "each wave a draft, each draft a different myth.\n\n"
        "His logbook lists the weather, not his thoughts —\n"
        "Force 8, south‑westerly, visibility poor.\n"
        "But between the data and the observation\n"
        "there is a man who stares and nothing more.\n\n"
        "The beam sweeps out and finds no ship tonight.\n"
        "He wonders if the light is for himself."
    ),
    "paper_boats.pdf": (
        "Paper Boats\n\n"
        "We made them from the morning newspaper,\n"
        "each vessel carrying yesterday's disasters\n"
        "across the puddle in the vacant lot.\n\n"
        "The headlines blurred and softened into pulp,\n"
        "the wars and weather folding into nothing\n"
        "as the water claimed them one by one.\n\n"
        "We did not mourn them.  Children never do.\n"
        "We simply tore another page and started."
    ),
    "cartography_of_scars.pdf": (
        "Cartography of Scars\n\n"
        "This one — the crescent on my left‑hand knuckle —\n"
        "belongs to a tin can opened wrong at twelve.\n"
        "That pale line running parallel to my wrist\n"
        "is where the rose bush argued with my shelf.\n\n"
        "I read my body like a foreign atlas,\n"
        "each mark a border drawn without my vote.\n"
        "The skin remembers what the mind lets go:\n"
        "a catalogue of every careless note.\n\n"
        "If you could map the damage that we carry,\n"
        "the world would look like one enormous scar —\n"
        "and somewhere under all the accumulated hurt,\n"
        "the country of who we actually are."
    ),
    "insomnia.pdf": (
        "Insomnia\n\n"
        "Three a.m.  The ceiling is a screen\n"
        "projecting all the conversations\n"
        "I should have had or should have left unspoken.\n\n"
        "The clock insists that time moves only forward,\n"
        "but my mind is a contraband machine\n"
        "that smuggles moments back across the border.\n\n"
        "I count the cars that pass — their headlights drawing\n"
        "brief parentheses of light across the wall.\n"
        "Someone, somewhere, has a reason to be driving.\n"
        "I have only reasons to be still."
    ),
    "the_unfinished_house.pdf": (
        "The Unfinished House\n\n"
        "My father built a house he never finished —\n"
        "the upstairs bedrooms open to the sky,\n"
        "the staircase climbing up to meet the weather.\n\n"
        "He said he'd get to it.  He always said\n"
        "that next month, next year, when the money came.\n"
        "It never came.  The rafters learned to rust.\n\n"
        "I think of him each time I leave a sentence\n"
        "without its final word, each time I start\n"
        "a project that I know I'll never —"
    ),
    "market_day.pdf": (
        "Market Day\n\n"
        "The mangoes come from somewhere I can't spell,\n"
        "stacked gold as sovereign coins beneath the awning.\n"
        "The vendor knows my name but not my sorrow,\n"
        "and that is all the distance that I need.\n\n"
        "She weighs the fruit the way you'd weigh a word\n"
        "before you say it — careful, almost tender.\n"
        "I leave with two kilos of summer in a bag\n"
        "and the quiet faith that sweetness can be purchased."
    ),
    "train_window.pdf": (
        "Train Window\n\n"
        "The landscape runs the other way, as if\n"
        "the earth itself is fleeing from the station.\n"
        "I press my forehead to the glass and watch\n"
        "a field of rapeseed burn in yellow silence.\n\n"
        "A farmhouse.  A tractor.  Someone else's life\n"
        "glimpsed for a second and forever lost.\n"
        "Travel is a long exercise in letting go\n"
        "of everything you didn't mean to notice."
    ),
    "small_gods.pdf": (
        "Small Gods\n\n"
        "There are gods in the hinge of the garden gate,\n"
        "in the crack where the pavement met the weeds.\n"
        "They govern nothing, answer no one's prayer,\n"
        "but they exist — as stubbornly as seeds.\n\n"
        "I've seen them in the static on the radio,\n"
        "in the ring a coffee cup leaves on a book.\n"
        "They ask for nothing.  They explain still less.\n"
        "They simply watch — and that's enough to look."
    ),
    "kitchen_hymn.pdf": (
        "Kitchen Hymn\n\n"
        "The onion splits in half and makes me cry,\n"
        "a sacrament of sulphur and of blade.\n"
        "The garlic pops in oil like tiny prayers\n"
        "ascending to the stovetop, undismayed.\n\n"
        "There is a liturgy to feeding people —\n"
        "the measuring, the stirring, and the wait.\n"
        "I learned my patience not in any temple\n"
        "but standing here, watching the hour grow late.\n\n"
        "Dinner is done.  The table set for four.\n"
        "Sometimes the holiest ground is just a floor."
    ),
    "after_rain.pdf": (
        "After Rain\n\n"
        "The street exhales.  The gutters run with light\n"
        "as puddles catch the neon from the shops.\n"
        "A child in yellow boots salutes the water,\n"
        "performing perfect, unselfconscious art.\n\n"
        "The air is clean the way a page is clean\n"
        "before the first word finds its way to ink.\n"
        "We stand beneath the dripping awning, waiting\n"
        "for nothing in particular, I think."
    ),
}

# ── Public domain classics ─────────────────────────────────────────────
PUBLIC_POEMS = {
    "shakespeare_sonnet_18.pdf": (
        "Sonnet 18 — William Shakespeare\n\n"
        "Shall I compare thee to a summer's day?\n"
        "Thou art more lovely and more temperate:\n"
        "Rough winds do shake the darling buds of May,\n"
        "And summer's lease hath all too short a date;\n\n"
        "Sometime too hot the eye of heaven shines,\n"
        "And often is his gold complexion dimm'd;\n"
        "And every fair from fair sometime declines,\n"
        "By chance or nature's changing course untrimm'd;\n\n"
        "But thy eternal summer shall not fade,\n"
        "Nor lose possession of that fair thou ow'st;\n"
        "Nor shall death brag thou wander'st in his shade,\n"
        "When in eternal lines to time thou grow'st:\n\n"
        "So long as men can breathe or eyes can see,\n"
        "So long lives this, and this gives life to thee."
    ),
    "dickinson_hope.pdf": (
        "'Hope' is the thing with feathers — Emily Dickinson\n\n"
        "'Hope' is the thing with feathers —\n"
        "That perches in the soul —\n"
        "And sings the tune without the words —\n"
        "And never stops — at all —\n\n"
        "And sweetest — in the Gale — is heard —\n"
        "And sore must be the storm —\n"
        "That could abash the little Bird\n"
        "That kept so many warm —\n\n"
        "I've heard it in the chillest land —\n"
        "And on the strangest Sea —\n"
        "Yet — never — in Extremity,\n"
        "It asked a crumb — of me."
    ),
    "frost_road_not_taken.pdf": (
        "The Road Not Taken — Robert Frost\n\n"
        "Two roads diverged in a yellow wood,\n"
        "And sorry I could not travel both\n"
        "And be one traveler, long I stood\n"
        "And looked down one as far as I could\n"
        "To where it bent in the undergrowth;\n\n"
        "Then took the other, as just as fair,\n"
        "And having perhaps the better claim,\n"
        "Because it was grassy and wanted wear;\n"
        "Though as for that the passing there\n"
        "Had worn them really about the same,\n\n"
        "And both that morning equally lay\n"
        "In leaves no step had trodden black.\n"
        "Oh, I kept the first for another day!\n"
        "Yet knowing how way leads on to way,\n"
        "I doubted if I should ever come back.\n\n"
        "I shall be telling this with a sigh\n"
        "Somewhere ages and ages hence:\n"
        "Two roads diverged in a wood, and I —\n"
        "I took the one less traveled by,\n"
        "And that has made all the difference."
    ),
    "blake_tyger.pdf": (
        "The Tyger — William Blake\n\n"
        "Tyger Tyger, burning bright,\n"
        "In the forests of the night;\n"
        "What immortal hand or eye,\n"
        "Could frame thy fearful symmetry?\n\n"
        "In what distant deeps or skies,\n"
        "Burnt the fire of thine eyes?\n"
        "On what wings dare he aspire?\n"
        "What the hand, dare seize the fire?\n\n"
        "And what shoulder, & what art,\n"
        "Could twist the sinews of thy heart?\n"
        "And when thy heart began to beat,\n"
        "What dread hand? & what dread feet?\n\n"
        "What the hammer? what the chain,\n"
        "In what furnace was thy brain?\n"
        "What the anvil? what dread grasp,\n"
        "Dare its deadly terrors clasp!\n\n"
        "When the stars threw down their spears\n"
        "And water'd heaven with their tears:\n"
        "Did he smile his work to see?\n"
        "Did he who made the Lamb make thee?\n\n"
        "Tyger Tyger burning bright,\n"
        "In the forests of the night:\n"
        "What immortal hand or eye,\n"
        "Dare frame thy fearful symmetry?"
    ),
    "keats_ode_nightingale.pdf": (
        "Ode to a Nightingale (excerpt) — John Keats\n\n"
        "My heart aches, and a drowsy numbness pains\n"
        "My sense, as though of hemlock I had drunk,\n"
        "Or emptied some dull opiate to the drains\n"
        "One minute past, and Lethe‑wards had sunk:\n\n"
        "'Tis not through envy of thy happy lot,\n"
        "But being too happy in thine happiness, —\n"
        "That thou, light‑wingéd Dryad of the trees,\n"
        "In some melodious plot\n"
        "Of beechen green, and shadows numberless,\n"
        "Singest of summer in full‑throated ease.\n\n"
        "Thou wast not born for death, immortal Bird!\n"
        "No hungry generations tread thee down;\n"
        "The voice I hear this passing night was heard\n"
        "In ancient days by emperor and clown."
    ),
    "whitman_o_captain.pdf": (
        "O Captain! My Captain! — Walt Whitman\n\n"
        "O Captain! my Captain! our fearful trip is done,\n"
        "The ship has weather'd every rack, the prize we sought is won,\n"
        "The port is near, the bells I hear, the people all exulting,\n"
        "While follow eyes the steady keel, the vessel grim and daring;\n\n"
        "But O heart! heart! heart!\n"
        "O the bleeding drops of red,\n"
        "Where on the deck my Captain lies,\n"
        "Fallen cold and dead.\n\n"
        "My Captain does not answer, his lips are pale and still,\n"
        "My father does not feel my arm, he has no pulse nor will,\n"
        "The ship is anchor'd safe and sound, its voyage closed and done,\n"
        "From fearful trip the victor ship comes in with object won."
    ),
}


def _sanitize(text: str) -> str:
    """Replace Unicode dashes / special chars with ASCII equivalents."""
    replacements = {
        "\u2010": "-",   # hyphen
        "\u2011": "-",   # non-breaking hyphen
        "\u2012": "-",   # figure dash
        "\u2013": "-",   # en dash
        "\u2014": "--",  # em dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote / apostrophe
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u00e9": "e",   # e-acute (winged)
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Fallback: encode to latin-1, replacing anything left
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _create_pdf(filepath: Path, text: str) -> None:
    """Write *text* to a single-page PDF at *filepath*."""
    text = _sanitize(text)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)
    for line in text.split("\n"):
        pdf.cell(0, 7, line, new_x="LMARGIN", new_y="NEXT")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(filepath))


def main() -> None:
    print("Generating sample poems …")

    for name, text in MY_POEMS.items():
        path = MY_DIR / name
        _create_pdf(path, text)
        print(f"  ✓ {path.relative_to(BASE_DIR)}")

    for name, text in PUBLIC_POEMS.items():
        path = PUB_DIR / name
        _create_pdf(path, text)
        print(f"  ✓ {path.relative_to(BASE_DIR)}")

    print(f"\nDone — {len(MY_POEMS)} original + {len(PUBLIC_POEMS)} classic poems created.")


if __name__ == "__main__":
    main()
