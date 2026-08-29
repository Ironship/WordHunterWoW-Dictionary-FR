# Audit script v3 - read keys from input to ensure correct apostrophes
cd C:\Users\Oleg\Desktop\WordHunterProjects\WordHunterWoW-Dictionary-FR

$inputPath = 'Data/cache/audit_work/in/batch_13.jsonl'
$outputPath = 'Data/cache/audit_work/out/batch_13.jsonl'

$input = Get-Content $inputPath -Encoding UTF8
$output = @()
$translationsChanged = 0
$notesWritten = 0

# Build audit hashtable from input, using actual keys
$audits = @{}

# Parse input to get actual keys
foreach ($line in $input) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $obj = $line | ConvertFrom-Json
    # Initialize all keys with their current translation and empty note
    $audits[$obj.key] = @{trans = $obj.current; note = ""}
}

# Now override with correct translations and notes
# Manual corrections - using actual keys from the input hashtable
$corrections = @{
    # Basic corrections
    "ingénieurs" = @{trans="engineers"; note="engineers; plural of ingénieur"}
    "ira" = @{trans="will go"; note="future tense of aller"}
    "jeux" = @{trans="games"; note="games or contests; entertainment in context"}
    "larves" = @{trans="larvae"; note="plural of larva; insect immature forms"}
    "libres" = @{trans="free"; note="freed or liberated; escaping imprisonment"}
    "lointain" = @{trans="distant"; note="far away or distant"}
    "observé" = @{trans="observed"; note="watched or observed; masculine past participle"}
    "ouverts" = @{trans="open"; note="open; masculine plural adjective"}
    "pairs" = @{trans="peers"; note="peers or equals; people of equal rank"}
    "paysage" = @{trans="landscape"; note="landscape or scenery"}
    "permanence" = @{trans="office"; note="permanence or office; the planner's post"}
    "progéniture" = @{trans="offspring"; note="offspring or progeny; descendants"}
    "prophétie" = @{trans="prophecy"; note="prophecy or prediction of future"}
    "protègent" = @{trans="protect"; note="protect or guard; 3rd person plural"}
    "préférée" = @{trans="favorite"; note="favorite or preferred; feminine"}
    "prélever" = @{trans="extract"; note="extract or take (teeth in context)"}
    "rappelez" = @{trans="recall"; note="recall or remember; imperative"}
    "rapporte" = @{trans="reports"; note="reports or tells; brings word"}
    "reconstruire" = @{trans="rebuild"; note="rebuild or reconstruct"}
    "regretter" = @{trans="regret"; note="regret or lament; infinitive"}
    "retentissants" = @{trans="Resounding"; note="resounding or magnificent"}
    "saison" = @{trans="season"; note="season; a period of time"}
    "sentez-vous" = @{trans="feel"; note="feel or sense; imperative"}
    "souffrent" = @{trans="suffer"; note="suffer or endure; 3rd person plural"}
    "stocks" = @{trans="stocks"; note="supplies or reserves"}
    "survivant" = @{trans="survivor"; note="survivor; sole survivor"}
    "s'étend" = @{trans="extends"; note="extends or spreads; reflexive 3rd person"}
    "tentatives" = @{trans="attempts"; note="attempts or tries; plural"}
    "traduit" = @{trans="translated"; note="translated; past participle"}
    "trous" = @{trans="holes"; note="holes or gaps; plural noun"}
    "variété" = @{trans="variety"; note="variety or type; particular kind"}
    "vend" = @{trans="sell"; note="sell or vend; 3rd person singular"}
    "vulnérables" = @{trans="vulnerable"; note="vulnerable or exposed; defenseless"}
    "éparpillées" = @{trans="scattered"; note="scattered or dispersed; feminine plural"}
    "affirme" = @{trans="asserts"; note="asserts or maintains; 3rd person"}
    "ancestrales" = @{trans="ancestral"; note="ancestral or of ancestors; feminine"}
    "annoncer" = @{trans="announce"; note="announce or proclaim; infinitive"}
    "antre" = @{trans="lair"; note="lair or den; beast's dwelling"}
    "apercevez" = @{trans="see"; note="see or glimpse; 2nd person present"}
    "appelez" = @{trans="call"; note="call or summon; imperative"}
    "approvisionner" = @{trans="supply"; note="supply or provision; infinitive"}
    "araignée" = @{trans="spider"; note="spider; arachnid"}
    "attaquée" = @{trans="attacked"; note="attacked or assailed; feminine"}
    "attendra" = @{trans="will wait"; note="will wait or will stay; future"}
    "bataillon" = @{trans="battalion"; note="battalion; military unit"}
    "boucher" = @{trans="block"; note="block or plug; seal or stop"}
    "bouge" = @{trans="moves"; note="moves or stirs; 3rd person singular"}
    "branche" = @{trans="branch"; note="branch or bough; tree limb"}
    "brasserie" = @{trans="brewery"; note="brewery or beer hall"}
    "carcasse" = @{trans="carcass"; note="carcass or skeleton; remains"}
    "cesser" = @{trans="cease"; note="cease or stop; infinitive"}
    "chambellan" = @{trans="chamberlain"; note="chamberlain; royal official"}
    "charmes" = @{trans="charms"; note="charms or talismans; magical objects"}
    "chauve-souris" = @{trans="bat"; note="bat (literally bald-mouse); flying mammal"}
    "chevaucheur" = @{trans="rider"; note="rider or mounted warrior"}
    "combattez" = @{trans="Fight"; note="fight or battle; imperative"}
    "complainte" = @{trans="Lament"; note="lament or dirge; mournful song"}
    "costaud" = @{trans="tough"; note="correction: tough, not strong; strong person"}
    "courrier" = @{trans="courier"; note="courier or messenger; mail carrier"}
    "couvées" = @{trans="broods"; note="broods or clutches; dragon offspring"}
    "critique" = @{trans="critical"; note="critical or grave; severe"}
    "dangereusement" = @{trans="dangerously"; note="dangerously; with danger"}
    "devoirs" = @{trans="duties"; note="correction: duties, not homework (context)"}
    "divine" = @{trans="divine"; note="divine or godly; of gods"}
    "donnez-leur" = @{trans="give them"; note="give them; imperative"}
    "dressent" = @{trans="stand"; note="stand or rise; 3rd person plural"}
    "dunes" = @{trans="dunes"; note="dunes; sand formations"}
    "débarrassez" = @{trans="get rid of"; note="get rid of or rid"}
    "déjouer" = @{trans="foil"; note="foil or thwart; defeat"}
    "dépouilles" = @{trans="remains"; note="remains or spoils; dead bodies"}
    "entoure" = @{trans="surrounds"; note="surrounds or encompasses; 3rd person"}
    "explosion" = @{trans="explosion"; note="correction: explosion, not blast"}
    "festivités" = @{trans="festivities"; note="festivities or celebrations"}
    "fichu" = @{trans="cursed"; note="correction: cursed or damned, not damn"}
    "filé" = @{trans="fled"; note="fled or ran away; past tense"}
    "fioles" = @{trans="vials"; note="vials or small bottles; containers"}
    "flot" = @{trans="flow"; note="flow or stream; current"}
    "flétrit" = @{trans="wilts"; note="wilts or withers; 3rd person"}
    "fonctionné" = @{trans="worked"; note="worked or functioned; past"}
    "forestier" = @{trans="forester"; note="forester or woodsman; ranger"}
    "glisser" = @{trans="slip"; note="slip or slide; infinitive"}
    "honore" = @{trans="honors"; note="honors or respects; 3rd person"}
    "horreur" = @{trans="horror"; note="horror or abomination; dread"}
    "impie" = @{trans="ungodly"; note="correction: ungodly, not impious"}
    "inférieur" = @{trans="lower"; note="lower or lower-level; comparative"}
    "intéressantes" = @{trans="interesting"; note="interesting or noteworthy; plural"}
    "intérêts" = @{trans="interests"; note="interests or concerns; plural"}
    "j'avoue" = @{trans="I admit"; note="I admit or I confess; 1st person"}
    "magnifiques" = @{trans="magnificent"; note="magnificent or splendid; plural"}
    "malade" = @{trans="sick"; note="sick or diseased; ill"}
    "messagers" = @{trans="messengers"; note="messengers or couriers; plural"}
    "mineur" = @{trans="minor"; note="minor or trivial; unimportant"}
    "mises" = @{trans="put"; note="put or placed; feminine plural"}
    "moisson" = @{trans="Harvest"; note="harvest or reaping; gathering"}
    "méchant" = @{trans="wicked"; note="wicked or evil; malicious"}
    "nérubien" = @{trans="nerubian"; note=""}
    "obtenez" = @{trans="get"; note="get or obtain; imperative"}
    "pandaren" = @{trans="pandaren"; note=""}
    "parvient" = @{trans="manages"; note="manages or succeeds; 3rd person"}
    "perturbation" = @{trans="disturbance"; note="disturbance or disruption"}
    "pillent" = @{trans="plunder"; note="plunder or loot; 3rd person"}
    "placés" = @{trans="placed"; note="placed or positioned; masculine plural"}
    "pouvaient" = @{trans="could"; note="could or were able; imperfect"}
    "probable" = @{trans="likely"; note="likely or probable"}
    "proposé" = @{trans="proposed"; note="proposed or suggested; past"}
    "péri" = @{trans="perished"; note="perished or died; past tense"}
    "quelconque" = @{trans="any"; note="any or ordinary; whatever"}
    "rater" = @{trans="miss"; note="miss or fail; lose an opportunity"}
    "ravages" = @{trans="ravages"; note="ravages or damage; destruction"}
    "rendue" = @{trans="rendered"; note="rendered or made; feminine"}
    "renforcé" = @{trans="reinforced"; note="reinforced or strengthened"}
    "requin" = @{trans="shark"; note="shark; predatory fish"}
    "niveaux" = @{trans="levels"; note="levels; plural of niveau"}
    "mettez-vous" = @{trans="position yourselves"; note="imperative: stand or position"}
    "mienne" = @{trans="mine"; note="possessive pronoun, feminine"}
    "parlerons" = @{trans="will speak"; note="correction: will speak, not let's talk (future tense)"}
    "secoue" = @{trans="shakes"; note="correction: shakes, not shaken (present tense)"}
    "élève" = @{trans="breeds"; note="correction: breeds or raises, not pupil (Legion context)"}
}

# Add corrections for elided words (with proper U+2019 apostrophes)
$ca = [char]0x2019
$elidedCorrections = @{
    "l${ca}abbaye" = @{trans="abbey"; note="elision: l' (the); abbey"}
    "l${ca}arbre-monde" = @{trans="World Tree"; note="World Tree (Yggdrasil); l' elision"}
    "n${ca}existe" = @{trans="does not exist"; note="elision: ne + existe; doesn't exist"}
    "s${ca}étend" = @{trans="extends"; note="extends or spreads; s' reflexive elision"}
    "d${ca}aussi" = @{trans="for as long"; note="d'aussi loin: as long as anyone remembers"}
    "d${ca}envahir" = @{trans="to invade"; note="to invade or assault; d' preposition"}
    "d${ca}ombrecroc" = @{trans="Shadowfang"; note=""}
    "j${ca}avoue" = @{trans="I admit"; note="I admit or I confess; j' = je elision"}
    "l${ca}amulette" = @{trans="amulet"; note="elision: l'amulette (the amulet); drop article"}
    "l${ca}orbite-sanglante" = @{trans="Bloody Orbit"; note="elision l'Orbite; proper noun"}
    "ohn${ca}ahra" = @{trans="Ohn'ahra"; note=""}
    "pa${ca}ku" = @{trans="Pa'ku"; note=""}
}

# Merge all corrections into audits
foreach ($key in $corrections.Keys) {
    if ($audits.ContainsKey($key)) {
        $audits[$key] = $corrections[$key]
    } else {
        # This shouldn't happen, but just in case
        Write-Host "Warning: Key '$key' not found in input"
        $audits[$key] = $corrections[$key]
    }
}

# Merge elided word corrections
foreach ($key in $elidedCorrections.Keys) {
    if ($audits.ContainsKey($key)) {
        $audits[$key] = $elidedCorrections[$key]
    } else {
        Write-Host "Warning: Elided key '$key' not found in input"
        $audits[$key] = $elidedCorrections[$key]
    }
}

# Now process each input line
foreach ($line in $input) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }

    $inObj = $line | ConvertFrom-Json
    $key = $inObj.key

    # Get audit data
    if ($audits.ContainsKey($key)) {
        $audit = $audits[$key]
        $newTrans = $audit.trans
        $note = $audit.note
    } else {
        $newTrans = $inObj.current
        $note = ""
    }

    # Track changes
    if ($newTrans -ne $inObj.current) {
        $translationsChanged++
    }
    if ($note -ne "") {
        $notesWritten++
    }

    # Create output object
    $outObj = [PSCustomObject]@{
        key = $inObj.key
        word = $inObj.word
        translation = $newTrans
        note = $note
    }

    $json = $outObj | ConvertTo-Json -Compress
    $output += $json
}

# Write output file with UTF-8 no BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($outputPath, $output, $utf8NoBom)

Write-Host "Rows written: $($output.Count)"
Write-Host "Translations changed: $translationsChanged"
Write-Host "Notes written: $notesWritten"
