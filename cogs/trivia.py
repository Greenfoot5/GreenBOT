import discord
from discord.ext import commands
import asyncio
import random
import pickle

'''
Initialisation
'''

#Colouring
def RankColour(rank):
        if rank == 1:
            return 0xFFFF11
        elif rank == 2:
            return 0xAAAAAA
        elif rank == 3:
            return 0x994400
        elif rank > 3 and rank <= 5:
            return 0x00FFFF
        elif rank > 5 and rank <= 10:
            return 0xFF3377
        elif rank > 10 and rank <= 25:
            return 0x00CC66
        elif rank > 25 and rank <= 50:
            return 0xCC4411
        elif rank > 50 and rank <= 100:
            return 0x990055
        elif rank > 100 and rank <= 250:
            return 0x9999FF
        else:
            return 0xFFFFFF
        
def is_module_enabled(module):
    """A :func`.check` that checks if the module is enabled on the server"""
    async def pred(ctx):
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        for a in range(len(guilds)):
            if guilds[a][0] == ctx.guild.id:
                if module == "misc":
                    if guilds[a][1][0] == True:
                        return True
                elif module == "trivia":
                    if guilds[a][2][0] == True:
                        return True
                elif module == "members":
                    if guilds[a][3][0] == True:
                        return True
    return commands.check(pred)


class TriviaCog:
    def __init__(self, bot):
        self.bot = bot
        self.TriviaList = [
            ["Who was the first woman pilot to fly solo across the Atlantic?",["Amelia Earhart"]],
            ["How many people have walked on the moon?",["12"]],
            ["What is the capital city of China?",["Beijing"]],
            ["What type of blood do you need to be a universal donor?",["O-"]],
            ["What is the chemical symbol for Helium?",["He"]],
            ["What is the author of The Hobbit and the Lord of the Rings trilogy's last name?",["Tolkien"]],
            ["SpaceX was founded by what South African-born inventor?",["Elon Musk"]],
            ["What is the capital city of Canada?",["Ottawa"]],
            ["Hale-Bopp is classified as which small Solar System body?",["Comet"]],
            ["What is the farthest human-made object from planet Earth?",["Voyager 1"]],
            ["Who played the female lead in the dystopian political thriller `V for Vendetta`?",["Natalie Portman"]],
            ["What is the favorite food of the Teenage Mutant Ninja Turtles?",["Pizza"]],
            ["What was the name of the teacher who dies in the tragic Space Shuttle Challenger disaster?",["Christa McAuliffe"]],
            ["Who led the first expedition to sail around the world?",["Ferdinand Magellan"]],
            ["Jules Verne's fictional submarine the Nautilus is captained by which character?",["Captain Nemo"]],
            ["The State of Israel was founded in what year?",["1948"]],
            ["What does HTTP stand for in a website address?",["HyperText transfer Protocol"]],
            ["In 1783, the first free flight of a hot air balloon carrying a human occured in what city?",["Paris"]],
            ["What did the famous Hollywood sign, located in Los Angeles, originally say?",["Hollywoodland"]],
            ["Which is the most abundant metal in the earth's crust?",["Aluminium"]],
            ["The Chihuahua is a breed of dog believed to originate from what country?",["Mexico"]],
            ["What is the largest island in the Caribbean Sea?",["Cuba"]],
            ["Which animal is the tallest in the world?",["Giraffe"]],
            ["What do you call a group of unicorns?",["A blessing"]],
            ["What is a baby rabbit called?",["Kitten"]],
            ["In science, what is an eon?",["1 billion years"]],
            ["Who was the lead singer of the band Audioslave?",["Chris Cornell"]],
            ["On the periodic table, what element has the symbol `K`?",["Potassium"]],
            ["In what year was the 4 minute mile first achieved?",["1954"]],
            ["What island does the Statue of Liberty stand on?",["Liberty Island"]],
            ["What is the name for the unity of measurement of power that is roughly equal to 746 watts?",["Horsepower"]],
            ["Who developed and patented the electrical telegraph in the US in 1837?",["Samuel Morse"]],
            ["In what country did table tennis originate?",["England"]],
            ["When adjusted for inflation, which is the highest grossing film of all time?",["Gone with the Wind"]],
            ["Who played the lead role in the 1982 American comedy Tootsie?",["Dustin Hoffman"]],
            ["Which country and it's territories cover the most time zones?",["France"]],
            ["How many time zones does France and it's territories cover?",["12"]],
            ["Which American writer writer wrote the narrative poem `The Raven`?",["Edgar Allan Poe"]],
            ["What is the capital city of Croatia?",["Zagreb"]],
            ["Pupusas, handmade thick stuffed corn tortillas, are a traditional dish from which country?",["El Salvador"]],
            ["New Orleans is known as the birthplace of what type of music?",["Jazz"]],
            ["Who was the male lead in the 1996 summer blockbuster Independence Day?",["Will Smith"]],
            ["The men's magazine GQ was formerly known by what longer name?",["Gentlemen's Quarterly"]],
            ["`Torchwoon` is an anagram and spin-off of what popular British sci-fi series?",["Doctor Who"]],
            ["What is the national animal of Scotland?",["Unicorn"]],
            ["The first McDonald's restaurant opened in which US state?",["California"]],
            ["Which shark is the biggest?",["Whale Shark"]],
            ["Actress Gal Gadot starred in what American superhero film released in the summer of 2017?",["Wonder Woman"]],
            ["In 1967, what band released the hit song `Ruby Tuesday`?",["The Rolling Stones"]],
            ["In the US, where can alligators and crocodiles be found together in the wild?",["South Florida"]],
            ["In which US state would you find Mount Rushmore?",["South Dakota"]],
            ["What is the second largest country by land mass?",["Canada"]],
            ["In which country is the Nobel Peace Prize awarded?",["Norway"]],
            ["How many items are in a bakers dozen?",["13"]],
            ["Who was the first actor to play Doctor Who in the television series?",["William Hartnell"]],
            ["How do you say `hello` in Swedish?",["Hej"]],
            ["What country has the largest land mass?",["Russia"]],
            ["The Artful Dodger is a character from which novel?",["Oliver Twist"]],
            ["`Au` is the symbol for what chemical element?",["Gold"]],
            ["What school does Harry Potter attend?",["Hogwarts"]],
            ["Wellington is the capital city of which island nation?",["New Zealand"]],
            ["Before the introduction of the euro, what was the name for the basic monetary unit used in the Netherlands?",["Guilder"]],
            ["What is the world's smallest country in terms of area?",["Vatican City"]],
            ["Who was the legendary Benedictine monk who invented champagne?",["Dom Perignon"]],
            ["Name the largest freshwater lake in the world?",["Lake Superior"]],
            ["Where would you find the Sea of Tranquility?",["The Moon"]],
            ["What is someone who shoes horses called?",["Farrier"]],
            ["What item of clothing was named after Scottish inventor?",["Mackintosh"]],
            ["What kind of weapon is a falchion?",["Sword"]],
            ["Which word goes before vest, beans and quartet?",["String"]],
            ["What is another word for lexicon?",["Dictionary"]],
            ["Which planet is 7th from the sun?",["Uranus"]],
            ["Who invented the rabies vaccination?",["Louis Pasteur"]],
            ["Which is the only American state to begin with the letter `p`?",["Pennsylvania"]],
            ["What is the world's longest river?",["Amazon"]],
            ["Which ocean is the largest?",["Pacific"]],
            ["What is the diameter of Terra in miles?",["8000"]],
            ["What is the capital of Spain?",["Madrid"]],
            ["Which country is Prague in?",["Czech Republic"]],
            ["Which English town was a forerunner of the Parks movement and the first city on Europe to have a street tram system?",["Birkenhead"]],
            ["Which actor starred in 142 films inluding: `The Quiet Man`, `The Shootist`, `The Searchers` and `Stagecoach`?",["John Wayne"]],
            ["Which film noir actress starred in: `I Married a Witch`, `The Glass Key`, `So Proudly We Hail!` and `Sullivan's Travels`?",["Veronica Lake"]],
            ["What is the oldest film ever made?",["Roundhay Garden Scene"]],
            ["What year was the oldest film made?",["1888"]],
            ["Which actress said, `Fasten your seatbelts. It's going to be a bumpy night,` in `All About Eve`?",["Bette Davis"]],
            ["Which character said, `Fasten your seatbelts. It's going to be a bumpy night,` in `All About Eve`?",["Margo Channing"]],
            ["Who directed `The Lord of the Rings` trilogy?",["Peter Jackson"]],
            ["Who played Neo in `The Matrix`?",["Keanu Reeves"]],
            ["Which actress' creer began at the age of 3, and who went on to star in films such as `Contact`, `Maverick` and `The Silence of the Lambs`?", ["Jodie Foster"]],
            ["Bray Studios, near Windsor in Berkshire, was home to which famous brand of horror films?", ["Hammer Horror"]],
            ["In which film did Humphrey Bogart say, `We'll always have Paris`?",["Casablanca"]],
            ["By what name is Lancelot Brown more usually known?",["Capability Brown"]],
            ["What is the name of the world famous gardens situated 10 miles (~ 16 km) outside London, close to the River Thames?",["Kew Gardens"]],
            ["Which popular gardener created Barnsdale Gardens and was the author of many books such as `The Ornamental Kitchen Garden`, `Gardeners World`, `Practical Gardening Course` and `Paradise Gardens`?",["Geoff Hamilton"]],
            ["Which garden is considered to be among the Seven Wonders of the Ancient World?",["The Hanging Gardens of Babylon"]],
            ["A Welsh poppy is what colour?",["Yellow"]],
            ["A Himalayan poppy is what colour?",["Blue"]],
            ["Which organic gardener is almost as famous for his long blond plait as he is for his books such as `Going Organic` and `The Gourmet Gardener` and his regular appearences on the BBC radio's `Gardener's Question Time`?",["Bob Flowerdew"]],
            ["What is an alternative name for the Mountain Ash tree?",["Rowan"]],
            ["Which kind of bulbs were once exchanged as a form of currency?",["Tulips"]],
            ["By which Latin name was Rosa Gallica previously known?",["Rosa Mundi"]],
            ["What colour jersey is worn by the current winner in each stage of the `Tour De France`?",["Yellow"]],
            ["Which heavyweight boxing champion finished his career with 49 fights without ever having been defeated?",["Rocky Marciano"]],
            ["Which sport does Constantino Rocca play?",["Golf"]],
            ["What country would you find the Cresta Run?",["Switzerland"]],
            ["How many times was the Men's Tennis Singles at Wimbledon won by Bjorn Borg?",["5"]],
            ["In 2011, which country hosted a Formula 1 race for the first time?",["India"]],
            ["What game is played on a lawn called a `crown green`?",["Bowls"]],
            ["Which chess piece can only move diagonally?",["Bishop"]],
            ["Which chess piece can only move in straight lines?",["Rook"]],
            ["Which chess piece can only move one space in any direction?",["King"]],
            ["Which chess piece can only move forwards unless capturing a piece?",["Pawn"]],
            ["Which chess piece move differently to the rest?",["Knight"]],
            ["Which chess piece can move in any direction any number of spaces?",["Queen"]],
            ["Which chess piece can become captured pieces?",["Pawn"]],
            ["Which footballer is the only one to have played for Liverpool, Everton, Manchester City and Manchester United?",["Peter Beardsley"]],
            ["In football, who was nicknamed `The Divine Ponytail`?",["Roberto Baggio"]],
            ["In needlework, what does UFO refer to?",["UnFinished Object"]],
            ["What was the name of the Russian ballet dancer who changed the face of modern baller?",["Rudolf Nureyev"]],
            ["What is the painting `La Gioconda` more usually known as?",["Mona Lisa"]],
            ["What does the term `piano` mean?",["To be played softly"]],
            ["Who was the Spanish artist, sculptor and draughtsman who was famous for co-founding the Cubist movement?",["Pablo Picasso"]],
            ["How many valves does a trumpet have?",["3"]],
            ["Who painted `How Sir Galahad, Sir Bors, and Sir Percival were Fed with the Sanc Grael; But Sir Percival's Sister Died by the Way?`",["Dante Gabriel Rossetti"]],
            ["If you were painting with tempera, what would you be using to bind together colour pigments?",["Egg yolk"]],
            ["What is John Leach famous for making?",["Pottery"]],
            ["When was William Shakespeare born?",["23/04/1564"]],
            ["On what date (DD/MM/YYYY) did the Battle of Culloden take place?",["16/04/1746"]],
            ["Who was `Henry VIII`'s first wife?",["Catherine of Aragon"]],
            ["Which famous battle between the British Royal Navy and the combined fleets of the French Navy and Spanish Navy took place on 21/10/1805?",["Battle of Trafalgar"]],
            ["Who became the British Prime Minister after Winston Churchill in 1955?",["Sir Robert Anthony Eden"]],
            ["What year did Maragret Thatcher become Prime Minister?",["1979"]],
            ["What year did the cold war end?",["1989"]],
            ["Who was the architect who designed the Millennium Dome?",["Richard Rogers"]],
            ["When did the Eurostar train service between Britain and France start running?",["14/11/1994"]],
            ["When was the euro introduced as legal currency on the world market?",["01/01/1999"]],
            ["What is the oldest surviving printed book in the world?",["The Diamond Sutra"]],
            ["What year is the oldest surviving printed book dated to?",["868"]],
            ["In publishing, what does POD mean?",["Print on demand"]],
            ["What author wrote `On Her Majesty's Secret Service` and `Thunderball` among others?",["Ian Fleming"]],
            ["Which Shakespeare play features Shylock?",["The merchant of Venice"]],
            ["Who wrote the novel `Death in Venice`, which was later made into a film by the same name?",["Thomas Mann"]],
            ["Who wrote the Vampire Chronicles, which include the novels: `Armand`, `Blood and Gold` and `Interview with the Vampire`?",["Anne Rice"]],
            ["How tall would a double elephant folio book be in inches?",["50"]],
            ["How many Roald Dahl books were publish including collections and books published after his death but not screenplays and plays?",["49"]],
            ["How many Roald Dahl books were for children?",["21"]],
            ["How many childrens novels did Roald Dahl write?",["18"]],
            ["How many short stories for adults did Rald Dahl write?",["18"]],
            ["How many adult novels did Roald Dahl publish?",["2"]],
            ["How many books of poetry for children did Roald Dahl write?",["3"]],
            ["Who wrote the contemporary children's books about mermaids set on the coast of Cornwall?",["Helen Dunmore"]],
            ["When was the world's oldest dictionary dated back to? (BC)",["2300"]],
            ["In `Thunderbirds`, what was Lady Penelope's chauffeur called?",["Parker"]],
            ["On `Blue Peter`, what was John Noakes's dog called?",["Shep"]],
            ["What BBC series was about a shipping line set in Liverpool during the late 1800s?",["The Onedin Line"]],
            ["Who invented TV?",["George Carey"]],
            ["What year was the idea for the TV first thought up?",["1876"]],
            ["What was the most watched UK TV programme of all time?",["Eastenders"]],
            ["When was the most watched UK TV programme aired?",["25/12/1986"]],
            ["Phyllis Nan Sortain Pechey was as famous for her flamboyant character as her cookery books and TV show throughout the late 1960s to the mid-1970s. By what name was she more ususally known?",["Fanny Cradock"]],
            ["Which popular BBC series about old collectables began in 1979 pesented by Bruce Parker and Arthur Negus, and is still running today?",["Antiques Roadshow"]],
            ["Which BBC music programme was broadcast weekly between 1964 and 2006?",["Top of the Pops"]],
            ["`Alistaire Burnett`, `Sandy Gall`, `Reginald Bosanquet`, `Alastair Stewart`, `Carol Barnes` and `Trevor McDonald` were all regular news presenters of which TV programme?",["ITV News at Ten"]],
            ["If you had Lafite-Rothschild on your dinner table, what would it be?",["Wine"]],
            ["What is sushi usually wrapped in?",["Seaweed"]],
            ["May Queen, Wisley Crab, Foxwelps and Lane's Prince Albert are all species of what?",["Apple"]],
            ["What is allspice alternatively known as?",["Pimenta"]],
            ["What colour is Absynthe?",["Green"]],
            ["What flavour is Cointreau?",["Orange"]],
            ["If you were to cut a hare into pieces, marinate it in wine and juniper berries then stew this slowly in a sealed container, what would this recipe be called?",["Jugged hare"]],
            ["How many crocus flowers does it take to make a pound of saffron?",["75000"]],
            ["Costing arounf $2600 per pound and only made to order by Knipschildt, what is the name of this chocolate truffle?",["Chocopologie"]],
            ["What nation was bounced from the Organisation of American States in 1962?",["Cuba"]],
            ["What continent has the fewest flowering plants?",["Antarctica"]],
            ["What element begins with the letter `K`?",["Krypton"]],
            ["What country saw a world record 315 million voters turn out for elections on May 20, 1991?",["India"]],
            ["What national holiday in Mexico has picnickers munching chocolate coffins and sugar skulls?",["Day of the Dead"]],
            ["What nation's military attached dynamite packs to Dobermans before sending them into Palestinian guerrilla hideouts?",["Israel"]],
            ["What was the first planet to be discovered using the telescope, in 1781?",["Uranus"]],
            ["How many days does cat usually stay in heat?",["5"]],
            ["How many US state border the Gulf of Mexico?",["5"]],
            ["What's the ballet termfor a 360-degree turn on one foot?",["Pirouette"]],
            ["What did blind bank robber David Worrell use a a weapon when trying to rob a London bank?",["His cane"]],
            ["What Great Lake state has more shoreline than the entire US Atlantic seaboard?",["Michigan"]],
            ["What model appeared topless on the self-penned 1993 novel Pirate?",["Fabio"]],
            ["Which country has more tractors per Capita?",["Iceland"]],
            ["Which country has the most Ph.D's per capita?",["China"]],
            ["Who averaged one patent for every three weeks on his life?",["Thomas Edison"]],
            ["What Elton John album became the first album to enter the charts a Number One, in 1975?",["Captain Fantastic and the Brown Dirt Cowboy"]],
            ["What laundry detergent got lots of mileage out of the ad line `ring around the collar`?",["Wisk"]],
            ["Who, after anchoring off Hawaii in 1779, was mistaken for the god Lono?",["Captain James Cook"]],
            ["What continent is cut into two fairly equal halves by the Tropic of Capricorn?",["Australia"]],
            ["What explorer introduced pigs to North America?",["Christopher Columbus"]],
            ["What magazine boasts the slogan: `Test, Inform, Protect`",["Consumer Reports"]],
            ["Who was killed as the `Killer of Custer` in Buffalo Bill's Wild West Show?",["Sitting Bull"]],
            ["What railway linked Moscow and Irkutsk in 1900?",["Trans-Siberian Railway"]],
            ["What is the minumum number of muscisians a band must have to be considered a `big band`?",["10"]],
            ["What's a water moccasinoften called, due to the white inside it's mouth?",["A cottonmouth"]],
            ["What word is defined in physics as a `nuclear reaction in which nuclei combine to form more massive nuclei`?",["Fusion"]],
            ["What's the largest and densest of the four rocky planets?",["Earth"]],
            ["What ingredient in fresh milk is eventually devoured by bacteria, causing the sour taste?",["Lactose"]],
            ["Who offered insurance against an accidental death caused by a falling Sputnik?",["Lloyd's of London"]],
            ["What is the world's largest island?",["Greenland"]],
            ["In what country would you find the world's most ancient forest?",["Australia"]],
            ["What is the name of the world's most ancient forest?",["Daintree Forest"]],
            ["With which sport is Michael Jordan associated?",["Basketball"]],
            ["`Churchill`, `Sherman` and `Panzer` were all developed as types of what?",["Tank"]],
            ["Which record label did Michael Jackson first record on?",["Motown"]],
            ["Who recoded the album `Dark Side Of the Moon`?",["Pink Floyd"]],
            ["Which Bobby took `Mack the Knife` to No 1 in the charts",["Darin"]],
            ["`My Heart Will Go On` came from which movie?",["Titanic"]],
            ["With which sport is Cedric Pioline associated?",["Tennis"]],
            ["What does the N stand for in `NATO`?",["North"]],
            ["Who played Rachel Green in `Friends`?",["Jennifer Aniston"]],
            ["Which instrument is Roberta Flack associated with?",["Piano"]],
            ["Who famously announced `heeeere's Johnny` on the Johnny Carson show from the early 60s?",["Ed McMahon"]],
            ["With what did ancient Romans dye their hair?",["Bird poo"]],
            ["On what continent did the samba originate?",["South America"]],
            ["Which fictional bear thought he has `very little brain`?",["Winnie the Pooh"]],
            ["Lord Mountbatten was murdered off the coast of which country?",["Ireland"]],
            ["In which US state was Isaac Hayes born?",["Tennessee"]],
            ["Black activist Steve Biko died in which country in the 70s?",["South Africa"]],
            ["What is the postal abbreviation for `Main`?",["ME"]],
            ["What was Aretha Franklin's first No 1?",["Respect"]],
            ["What is the main colour on the Chinese flag?",["Red"]],
            ["Dick Francis novels revolve around which sport?",["Horse racing"]],
            ["What does the `C` stand for in `LCD`?",["Crystal"]],
            ["In which country did marilyn Monroe die?",["US","USA","United States","United States of America"]],
            ["Which Danny starred in Batman Returns?",["De Vito"]],
            ["In which US state is Prince William Sound?",["Alaska"]],
            ["What followed Exhale in the 1995 Whitney Houston hit?",["Shoop Shoop"]],
            ["Which sitcom about an army hospital in Korea was transmitted in the UK without the canned laughter of the US version?",["M*A*S*H"]],
            ["The disatrous poison gas leak at Bhopal took place in which counrtry?",["India"]],
            ["Which Sinatra song manages to rhyme a line with `shy way`?",["My Way"]],
            ["Which is which decade was Andie MacDowell born?",["1950s"]],
            ["What sort of Nest was the subject of over 150 sitcoms?",["Empty"]],
            ["What type of cargo was carried by the stricken vessel `The Torrey Canyon`?",["Oil"]],
            ["Playwrite Arthur Miller was married to which famous blond actress?",["Marilyn Monroe"]],
            ["In American football, where do the Broncos come from?",["Denver"]],
            ["Which actress married for the seventh time on Michael Jackson's ranch in 1991?",["Elizabeth Taylor"]],
            ["Hartsfield international airport is in which US state?",["Georgia"]],
            ["What game was created by French mathematician Blaise Pascal, which he discovered when doing experiments into perpetual motion?",["Roulette"]],
            ["Who said `I'm the president of the United States and I'm not going to eat any more broccoli`?",["George Bush"]],
            ["What so-called `war` spawned the dueling of slogans `Better Dead Than RED` and `Better Red than Dead`?",["Cold War"]],
            ["In which year were TV licenses introduced in the UK?",["1946"]],
            ["Which designer (brand) created the Kelly bag?",["Hermes"]],
            ["`Arctic King`, `Saladin` and `Tom Thumb` are all types of what?",["Lettuce"]],
            ["By what neame is the Gravelly Hill interchange better known?",["Spaghetti Junction"]],
            ["The Galápagos Islands are a provincial territory of which South American counrty?",["Ecuador"]],
            ["Which Gilbert and Sullivan operetta is sub-titled `The Slave of Duty`?",["The Pirates of Penzance"]],
            ["Who succeeded Sir Clive Woodward as England's rugby union coach?",["Andy Robinson"]],
            ["What is a baby oyster called?",["Spat"]],
            ["What is Bill Clinton's middle name?",["Jefferson"]],
            ["In which country are the Sutherland Falls?",["New Zealand"]],
            ["In the US TV comedy show `Everybody Loves Raymond`, what is Raymond's brother's first name?",["Robert"]],
            ["What is the largest flat fish species?",["Halibut"]],
            ["Apart from a battle, what did Nelson lose at Tenerife in 1797?",["His right arm"]],
            ["What's the oldest university in the US",["Havard"]],
            ["Who became Germany's first female chancellor?",["Angela Markel"]],
            ["Who wrote `The Railway Children`?",["Edith Nesbit"]],
            ["Who played the `Ringo Kid` in the original stagecoach film?",["John Wayne"]],
            ["Which artist painted `The Potato Eaters`?",["Vincent van Gogh"]],
            ["In architecture, what is a lancet?",["Window"]],
            ["Which singer's original name was Elaine Bookbinder?",["Elkie Brooks"]],
            ["Turin lines on which river?",["Po"]],
            ["Which country has the international car registation `RA`?",["Argentina"]],
            ["A methuselah of wine holds the equivalent of how many bottles?",["8"]],
            ["Launched in 1960, what was the ame of the first US communications satellite?",["Echo 1"]],
            ["Who invented jeans?",["Levi Strauss"]],
            ["What does a cartophilist collect?",["Cigarette cards"]],
            ["Which European city had the Roman name Lutetia?",["Paris"]],
            ["What is the green pigment found in most plants that is responsible for absorbing light energy?",["Chlorophyll"]],
            ["Yeomen Warders at the Tower of London are commonly known by what other name?",["Beefeaters"]],
            ["Which actress appears with Jarvis Cocker in Pulp's video, `Common People`?",["Sadie Frost"]],
            ["How many labours were performed by Herclues?",["12"]],
            ["Which late MP owned Saltwood Castle in Kent?",["Alan Clarke"]],
            ["In which London pub did Ronnie Kray murder George Cornell?",["The Blind Begger"]],
            ["What day and month is Trafalgar Day?",["21/10"]],
            ["What is the birthstone for April?",["Diamond"]],
            ["What does `E` represent in `E = MC^2`?",["Energy"]],
            ["What note do orchestras typically tune up to?",["A"]],
            ["Which English cathedral was destroyed by fire in 1666?",["St Paul's"]],
            ["Who shot and killed Billy the Kid in 1881?",["Pat Garrett"]],
            ["What was the first name of Dustin Hoffman's female character in `Tootsie`?",["Dorothy"]],
            ["Which UK store was first to have an escalator installed?",["Harrods"]],
            ["In which year were luncheon vouchers introduced on the Uk?",["1955"]],
            ["How did soul singer Otis Redding die in 1967?",["Plane crash"]],
            ["Who invented the revolver?",["Samuel Colt"]],
            ["In which ocean is `Ascension Island`?",["Atlantic"]],
            ["What is the US state capital of California?",["Sacramento"]],
            ["In which country was cricketer Ted Dexter born?",["Italy"]],
            ["Who was the first English monarch to abdicate? (Use Roman numerals so, 1 = I, 2 = II, 3 = III, ect.)",["Richard II"]],
            ["At which railway station was the film `Brief Encounter` made?",["Carnforth"]],
            ["Who was the first British person to walk in space?",["Michael Foale"]],
            ["Miss Gatsby and Miss Tibbs were two elderly residents in which UK tv sitcom?",["Fawlty  Towers"]],
            ["What is the postcode for BBC’s soap `Eastenders`?",["E20"]],
            ["Which country has won the most medals in total at the Summer Olympic Games?",["US","USA","United States","United States of America"]],
            ["Which US burlesque dancer and model was born Heather Renee Sweet?",["Dita Von Teese"]],
            ["Who invented the jet engine in 1930?",["Frank Whittle"]],
            ["What is the US state capital of Mississippi?",["Jackson"]],
            ["What is Earth's atmospheric region of charged particles connecting the stratosphere, mesosphere and thermosphere?",["Ionosphere"]],
            ["Which artist said, `When we love a woman we don't start measuring her limbs`?",["Pablo Picasso"]],
            ["What was Manfred von Richtofen's nickname?",["The Red Baron"]],
            ["What does a vexillogist study?",["Flags"]],
            ["Which is the largest of the Channel Islands?",["Jersey"]],
            ["Who wrote `Far From The Madding Crowd`?",["Thomas Hardy"]],
            ["Who plays Grace in the US sitcom `Will and Grace`?",["Debra Messing"]],
            ["At which golf course does the US Masters take place?",["Augusta"]],
            ["What does `NATO` stand for?",["North Atlantic Treaty Organization"]],
            ["Which is the largest Castle in England?",["Windsor Castle"]],
            ["In the Western world, commonly in which month of the year is All Saints' Day?",["November"]],
            ["In which English cathedral is the Bell Harry Tower?",["Canterbury"]],
            ["In which country was exiled Russian Leader `Leon Trotsky` killed in 1940?",["Mexico"]],
            ["In what year did exiled Russian Leader `Leon Trotsky` get killed in Mexico?",["1940"]],
            ["Who played Simon Templar in the 1997 film `The Saint`?",["Val Kimler"]],
            ["Which European country has the roman name Helvetia?",["Switzerland"]],
            ["Which fashion items does Jimmy Choo design?",["Shoes"]],
            ["What is a blini?",["Pancake"]],
            ["If a dish is `a la crecy` with what is it garnished?",["Carrots"]],
            ["Which country has the international car registration `ET`? (No, not aliens)",["Egypt"]],
            ["What is the currency of Albania?",["Lek"]],
            ["Which 1950's singer was originally Charles Hardin?",["Buddy Holly"]],
            ["Which London station was designed by `Sir George Gilbert Scott`?",["St Pancras"]],
            ["Which bird was names after engraver `Sir Thomas Bewick`?",["Bewick Swan"]],
            ["What is the number 3.141... normally known as?",["Pi"]],
            ["What is Pi to 15 decimal places?",["3.141592653589793"]],
            ["In the Greek Alphabet, what position is Pi?",["16"]],
            ["Who scored England's first goal in the 1998 World Cup Final tournament?",["Alan Shearer"]],
            ["Which is the largest of the Great Lakes?",["Lake Superior"]],
            ["Which British Prime Minister had a bag named after them?",["Gladstone"]],
            ["`Majestic`, `Romano` and `Arran Victory` are types of which vegtable?",["Potato"]],
            ["A firkin beer holds how many gallons?",["9"]],
            ["What is the title of the film about a Scottish village that awakens once every 100 years?",["Brigadoon"]],
            ["In which year did Roger Bannister break the four-minute mile?",["1964"]],
            ["In 1964 a sub four-minute mile was completed, but by whom?",["Roger Bannister"]],
            ["In 1960 Dr Thomas Creighton was the first person to recieve what punishment?",["Parking Ticket"]],
            ["In what year was the first parking ticket issued?",["1960"]],
            ["In which country was actor Mel Gibson born?",["US","USA","United States","United States of America"]],
            ["Whose autobiography is entitled `Take It Like A Man`?",["Boy George"]],
            ["What is the lightest metal?",["Lithium"]],
            ["What is the letter 9th letter of the Greek Alphabet?",["Iota"]],
            ["Iota is a letter of the Greek Alphabet but what is it's position?",["9"]],
            ["What is the Farenheit boiling point of water?",["212"]],
            ["What is 212 Farenheit in Celcius?",["100"]],
            ["How many sides does a rhombus have?",["4"]],
            ["Which is the smallest bone in the body?",["Stirrup"]],
            ["What is Adam's Ale commonly known as?",["Water"]],
            ["```\nA dozen a gross and a score,\nplus three times the square root of four,\ndivided by seven,\nplus five times eleven,\nis nine squared and not a bit more.\n```\nThis is an example of what?",["Limerick"]],
            ["How many syllables are in a Haiku?",["17"]],
            ["Who served the longest time in office as Poet Laureate?",["Alfred Tennyson"]],
            ["How many years did Alfred, Lord Tennyson serve as Poet Laureate?",["42"]],
            ["Which is the oldest football club in London?",["Fulham"]],
            ["There are two ingredients in Bellini cocktail. Champagne and what?",["Peach Juice"]],
            ["There are two ingredients in Bellini cocktail. Peach Juice and what?",["Champagne"]],
            ["Which playwright wrote `The Cricible`?",["Arthur Miller"]],
            ["What to algophobics fear?",["Pain"]],
            ["If a creature is `opoduous` what has it not got?",["Feet"]],
            ["What chemical element has the atomic number 18?",["Argon"]],
            ["What is the atomic number for the element Argon?",["18"]],
            ["What is the name of the character played by Angela Lansbury in `Murder, She Wrote`?",["Jessica Fletcher"]],
            ["Who played Jessica Fletcher in `Murder, She Wrote`?",["Angela Lansbury"]],
            ["What is the name of the hooked staff carried by a bishop?",["Crozier"]],
            ["In which war was Agent Orange used by the US?",["Vietnam"]],
            ["Who was the Greek God of dreams?",["Morpheus"]],
            ["What was boxer Barry McGuigan's weight division?",["Featherweight"]],
            ["What is `nacre` commonly known as?",["Mother of Pearl"]],
            ["What is the fictional brewery associated with the Rovers Return pub in TV's Coronation Street series?",["Newton and Ridley"]],
            ["What colour is the Mr Men character Mr Tall?",["Blue"]],
            ["What does a hippophobic fear?",["Horses"]],
            ["Where is the Royal Navy Officer Training School?",["Dartmouth"]],
            ["What is the best-selling book in the US?",["Bible"]],
            ["What is the best-selling book in the US after the Bible?",["Dr Spock's Baby and Child Care"]],
            ["Who had a hit single in the 1960's with `Light My Fire`?",["The Doors"]],
            ["In which ocean are the Cape Verde islands?",["Atlantic"]],
            ["How many bones are there in the human body?",["206"]],
            ["What is the Lonicera plant commonly known as?",["Honeysuckle"]],
            ["`Rule Britannia` is the work of which composer?",["Thomas Arne"]],
            ["What does a `vigneron` cultivate?",["Grapes"]],
            ["Which creature in Greek mythology was half-man and half-bull?",["Minotaur"]],
            ["The battle of Alma was fought in september of what year?",["1854"]],
            ["The battle of Alma was fought during which war?",["Crimean War"]],
            ["How much does Michael Henchard sell his wife and daughter for in Thomas Hardy's novel `The Mayor of Casterbridge`?",["5 Guineas"]],
            ["What are the two ingredients in a Rustly Nail cocktail?",["Drambuie and Whiskey","Whiskey and Drambuie","Drambuie, Whiskey","Whiskey, Drambuie","Drambuie Whiskey","Whiskey Drambuie"]],
            ["Who became the first `Children's Laureate` in 1999?",["Quentin Blake"]],
            ["How many players are there in a netball team?",["7"]],
            ["Who was the first poet to be buried in Poets Corner in London's Westminster Abbey?",["Geoffrey Chaucer"]],
            ["What is the fifth letter of the Greek alphabet?",["Epsilon"]],
            ["Which comedian's autobiography is entitled `The Full Monty`?",["Jim Davidson"]],
            ["Introduced in New York in 1950 what was the first credit card?",["Diners Club"]],
            ["Which is the longest mountain range in the world?",["The Andes"]],
            ["In kilometers, how long is the longest mountain range?",["7240"]],
            ["What kind of fruit would you pick from a Mirabelle tree?",["Plum"]],
            ["Who was Britain's first Labour Prime Minister?",["Ramsey MacDonald"]],
            ["Who painted `The laughing Cavalier`?",["Franz Hals"]],
            ["Which famous guitarist's original name was Brian Rankin?",["Hank Marvin"]],
            ["What iconic symbol is the long-standing trademark and clip design of `Parker Pen Co`?",["Arrow"]],
            ["With what is Earl Grey tea flavoured?",["Bergamot"]],
            ["What number is a hurricane on the Beaufort Scale?",["12"]],
            ["Who directed the film `Alien`?",["Ridley Scott"]]
            ]          
        self.TriviaServers = []
        self.restarting = False

    @commands.group(name="tr",aliases=["trivia","Tr","Trivia"])
    @is_module_enabled('trivia')
    async def tr(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("To find out how to use the trivia command run `&&help trivia`")
    
    @tr.command(name="start")
    async def trstart(self,ctx):
        if ctx.guild.id in self.TriviaServers:
            await ctx.send("A game is already running.")
            return
        if self.restarting == True:
            await ctx.send("Bot will be restarting soon. Please wait 5 minutes and then run the command again. The bot should have restarted in that time.")
            return
        self.TriviaServers.append(ctx.guild.id)
        await ctx.send("Trivia starting in 5...")
        await asyncio.sleep(5)
        unanswered = 0
        MessageAuthor = ctx.author
        print('Tr Start')
        while ctx.guild.id in self.TriviaServers:
            if self.restarting == True:
                await ctx.send("Bot will be restarting soon. Please wait 6 minutes and then run `&&tr start` command again to begin. The bot should have restarted in that time.")
                return
            channel = ctx.channel
            question = random.randint(0,len(self.TriviaList)-1)
            await channel.send(content=self.TriviaList[question][0],delete_after=300)
            def check(m):
                MessageAuthor = m.author
                for b in range(len(self.TriviaList[question][1])):
                    if m.content.lower() == self.TriviaList[question][1][b].lower():
                        return m.channel == channel and m.author != self.bot.user and True
                return False

            try:
                guess = await self.bot.wait_for('message', check=check, timeout=20.0)
                await ctx.send(content="{} got it right!".format(guess.author.mention),delete_after=300)
                unanswered = 0
                TLB = pickle.load(open("triviaLB.data", "rb"))
                added = False
                for y in range(len(TLB)):
                    if TLB[y][0] == (guess.author.id):
                        TLB[y][1] += 1
                        added = True
                if added == False:
                    TLB.append([guess.author.id,1])
                def getKey(item):
                    return item[1]
                TLB = sorted(TLB,reverse=True,key=getKey)
                pickle.dump(TLB, open('triviaLB.data','wb'))
                CoinList = []
                CoinList = pickle.load(open('Coin.data', 'rb'))
                added = False
                Reward = 1
                for y in range(len(CoinList)):
                    if CoinList[y][0] == (ctx.author.id):
                        added = True
                        placement = y
                        break
                if added == False:
                    placmement = len(CoinList)
                    CoinList.append([ctx.author.id,Reward,0,0,0])
                if added == True:
                    CoinList[placement][1] +=  Reward
                def getKey(item):
                    return item[1]
                CoinList = sorted(CoinList,reverse=True,key=getKey)
                for y in range(len(CoinList)):
                    if CoinList[y][0] == (ctx.author.id):
                        placement = y
                pickle.dump(CoinList, open('Coin.data','wb'))
            except asyncio.TimeoutError:
                answer = '`' + self.TriviaList[question][1][0] + '`'
                await ctx.channel.send(content=f'Sorry, you took too long it was {answer}.',delete_after=300)
                unanswered += 1
            if unanswered == 7:
                await ctx.send("Too many questions unanswered. Stopping the Trivia.")
                self.TriviaServers.remove(ctx.guild.id)
                print("Tr Stop")

    @tr.command(name="length",aliases=["l","L","Length"])
    async def trlen(self,ctx):
        text = str(len(self.TriviaList)) + " questions"
        await ctx.send(text)

    @tr.command(name='stats')
    async def trStats(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        if ctx.guild == None:
            return
        TLB = []
        TLB = pickle.load(open('triviaLB.data', 'rb'))
        added = False
        for y in range(len(TLB)):
            if TLB[y][0] == (member.id):
                added = True
                placement = y
                break
        if added == True:
            embed = discord.Embed(title="Stats for",
                              description=member.name,
                              colour=RankColour(placement))
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='png'))
            embed.add_field(name='Rank',
                        value=(placement))
            embed.add_field(name='Correct Trivia answers',
                            value=(TLB[placement][1]))
            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='**Displaying user trivia stats**', embed=embed)
        if added == False:
            await ctx.send("User hasn't got a trivia answer correct yet.")

    @tr.command(name='rank')
    async def trRank(self, ctx, placement:int=None):
        if ctx.guild == None:
            return
        if placement == None:
            placement = 1
        TLB = []
        TLB = pickle.load(open('triviaLB.data', 'rb'))
        added = False
        if (placement) >= len(TLB) or placement < 1:
            await ctx.send("There isn't a person at that rank.")
            return
        
        member = self.bot.get_user(int(TLB[placement][0]))
        embed = discord.Embed(title="Stats for",
                              description=member.display_name,
                              colour=RankColour(placement))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))

        embed.add_field(name='Rank',
                        value=(placement))
        embed.add_field(name='Correct Trivia answers',
                        value=(TLB[placement][1]))
        if placement == 1:
            embed.add_field(name='Correct answers to next rank',
                            value="They are #1!")
        else:
            embed.add_field(name='Correct answers to next rank',
                            value=((TLB[placement-1][1])-(TLB[placement][1]))+1)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying rank stats**', embed=embed)

    @tr.command(name='top')
    async def trTop(self,ctx):
        if ctx.guild == None:
            return
        TLB = []
        TLB = pickle.load(open('triviaLB.data','rb'))
        placement = 1
        value1 = "•**name:** "+str(self.bot.get_user(TLB[1][0]).name)+"\n•**Correct Trivia Answers:** "+str(TLB[1][1])
        value2 = "•**name:** "+str(self.bot.get_user(TLB[2][0]).name)+"\n•**Correct Trivia Answers:** "+str(TLB[2][1])
        value3 = "•**name:** "+str(self.bot.get_user(TLB[3][0]).name)+"\n•**Correct Trivia Answers:** "+str(TLB[3][1])
        value4 = "•**name:** "+str(self.bot.get_user(TLB[4][0]).name)+"\n•**Correct Trivia Answers:** "+str(TLB[4][1])
        value5 = "•**name:** "+str(self.bot.get_user(TLB[5][0]).name)+"\n•**Correct Trivia Answers:** "+str(TLB[5][1])
        embed = discord.Embed(title="Top trivia players",
                              description="Top ranks",
                              colour=0x663311)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='#1',
                        value=value1)
        embed.add_field(name='#2',
                        value=value2)
        embed.add_field(name='#3',
                        value=value3)
        embed.add_field(name='#4',
                        value=value4)
        embed.add_field(name='#5',
                        value=value5)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying top trivia players**', embed=embed)    

    @commands.command('tr_restart')
    @commands.is_owner()
    async def tr_restart(self,ctx):
            self.restarting = True
            await asyncio.sleep(360)
            print('Restart')
            self.restarting = False
            
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(TriviaCog(bot))
    random.seed()
