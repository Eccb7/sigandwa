"""
Ussher's Annals of the World - Comprehensive Seed Data
Extended Biblical Timeline from James Ussher's chronology (1650)
with integration of Daniel's prophecies and historical continuation
"""

USSHER_ANNALS_EVENTS = [
    # CREATION ERA - 4004 BC
    {
        "name": "Creation of the World",
        "description": "God created heaven and earth. The beginning of time occurred at the start of evening preceding October 23rd, 4004 BC in the Julian calendar. On the first day, God created the highest heaven and angels, fashioned the lower globe consisting of the deep and earth, and created light dividing it from darkness.",
        "year_start": -4004,
        "year_end": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 1:1-5",
        "key_actors": ["God"],
        "source_references": ["Ussher Annals AM 1a, JP 710"],
        "extra_data": {
            "ussher_date": "October 23, 4004 BC",
            "annals_reference": "1a AM, 710 JP",
            "significance": "absolute_beginning",
            "confidence": "high"
        }
    },
    {
        "name": "Creation Week - Day 2",
        "description": "God created the firmament (heaven) and separated waters above from waters below enclosing the earth",
        "year_start": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 1:6-8",
        "key_actors": ["God"],
        "source_references": ["Ussher Annals - October 24, 4004 BC"],
        "extra_data": {"day": "Monday, October 24, 4004 BC"}
    },
    {
        "name": "Creation Week - Day 3",
        "description": "God gathered waters into seas, dry land appeared, and earth brought forth all kinds of herbs and plants. The Garden of Eden was enriched with plants including the tree of life and tree of knowledge of good and evil.",
        "year_start": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 1:9-13, Genesis 2:8-9",
        "key_actors": ["God"],
        "source_references": ["Ussher Annals - October 25, 4004 BC"],
        "extra_data": {"day": "Tuesday, October 25, 4004 BC"}
    },
    {
        "name": "Creation Week - Day 4",
        "description": "God created the sun, moon, and stars",
        "year_start": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 1:14-19",
        "key_actors": ["God"],
        "source_references": ["Ussher Annals - October 26, 4004 BC"],
        "extra_data": {"day": "Wednesday, October 26, 4004 BC"}
    },
    {
        "name": "Creation Week - Day 5",
        "description": "God created fish and flying birds, commanding them to multiply and fill the sea and earth",
        "year_start": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 1:20-23",
        "key_actors": ["God"],
        "source_references": ["Ussher Annals - October 27, 4004 BC"],
        "extra_data": {"day": "Thursday, October 27, 4004 BC"}
    },
    {
        "name": "Creation Week - Day 6: Man Created",
        "description": "God created living creatures of the earth and creeping creatures. Finally, man was created in God's image with divine knowledge and natural sanctity. Adam named all creatures and God created Eve from Adam's rib. God blessed them, gave them dominion over all living creatures, and provided food. All creation was declared very good.",
        "year_start": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 1:24-31, Genesis 2:18-25, Colossians 3:10, Ephesians 4:24",
        "key_actors": ["God", "Adam", "Eve"],
        "source_references": ["Ussher Annals - October 28, 4004 BC"],
        "extra_data": {
            "day": "Friday, October 28, 4004 BC",
            "significance": "creation_of_mankind"
        }
    },
    {
        "name": "Creation Week - Day 7: First Sabbath",
        "description": "God rested from all His work. He blessed the seventh day and ordained the Sabbath as a sign of sanctification and foreshadowing eternal rest from sin and punishment. This day was set forth as a sign of eternal sabbath to be enjoyed in the world to come.",
        "year_start": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 2:2-3, Exodus 31:13,17, Hebrews 4:4,9-10",
        "key_actors": ["God"],
        "source_references": ["Ussher Annals - October 29, 4004 BC"],
        "extra_data": {
            "day": "Saturday, October 29, 4004 BC",
            "significance": "first_sabbath_rest"
        }
    },
    {
        "name": "The Fall of Man",
        "description": "The Devil, envied God's honor and man's obedience, tempted Eve through the serpent. Eve was deceived and Adam seduced to break God's command about the forbidden fruit. God pronounced judgment on the serpent, woman, and man. God promised that the seed of the woman would crush the serpent's head - Christ would undo the devil's works. Adam named his wife Eve as mother of all living and of those who would live by faith in the promised Messiah.",
        "year_start": -4004,
        "year_start_min": -4004,
        "year_start_max": -4000,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 3:1-20, Revelation 12:9, Revelation 20:2, 1 John 3:8, Romans 16:20, 1 Peter 3:6, Galatians 4:31",
        "key_actors": ["Satan", "Eve", "Adam", "God"],
        "source_references": ["Ussher Annals AM 1"],
        "extra_data": {
            "consequence": "sin_death_entered_world",
            "pattern": "disobedience_judgment_promise",
            "proto_evangelium": "first_gospel_promise"
        }
    },
    {
        "name": "Expulsion from Eden",
        "description": "Adam and Eve were clothed by God with garments of skins and expelled from the Garden of Eden. A flaming sword was set to guard the way to the tree of life. Likely occurred on the 10th day of the world (November 1st). This day later became the Day of Atonement, a yearly fast where Israelites were commanded to afflict their souls.",
        "year_start": -4004,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 3:21-24, Leviticus 16:29, Leviticus 23:27-29, Acts 27:9",
        "key_actors": ["God", "Adam", "Eve"],
        "source_references": ["Ussher Annals AM 1, November 1st"],
        "extra_data": {
            "ussher_date": "November 1, 4004 BC",
            "day_of_world": 10,
            "future_significance": "day_of_atonement_established"
        }
    },
    {
        "name": "Birth of Cain",
        "description": "Cain was born, the first of all mortal men born of a woman after the Fall",
        "year_start": -4004,
        "year_start_min": -4004,
        "year_start_max": -3875,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 4:1",
        "key_actors": ["Eve", "Cain"],
        "source_references": ["Ussher Annals AM 1"],
        "extra_data": {"significance": "first_human_birth"}
    },
    {
        "name": "Murder of Abel",
        "description": "Cain murdered his brother Abel - the first human death by violence. With an estimated 500,000 people on earth after 128 years, Cain feared vengeance from others for his crime. This marked the first recorded murder and pattern of violence escalation.",
        "year_start": -3875,
        "year_start_min": -3900,
        "year_start_max": -3850,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 4:8,14-15",
        "key_actors": ["Cain", "Abel"],
        "source_references": ["Ussher Annals 130d AM, 840 JP"],
        "extra_data": {
            "annals_reference": "130d AM, 840 JP",
            "pattern": "violence_escalation",
            "estimated_population": 500000,
            "significance": "first_murder"
        }
    },
    {
        "name": "Birth of Seth",
        "description": "God gave Eve another son named Seth after Abel's murder. Adam was 130 years old. Seth was given as a replacement for Abel, indicating no other sons were born to Eve between Abel's death and Seth's birth.",
        "year_start": -3874,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 4:25, Genesis 5:3-4",
        "key_actors": ["Adam", "Eve", "Seth"],
        "source_references": ["Ussher Annals 130d AM, 840 JP"],
        "extra_data": {
            "annals_reference": "130d AM, 840 JP",
            "adam_age": 130
        }
    },
    {
        "name": "Birth of Enos - Worship Corruption Begins",
        "description": "When Seth was 105 years old, his son Enos was born. By this time, the worship of God had been wretchedly corrupted by the race of Cain. This marks when men began to be distinguished between those who called upon the name of the Lord and those who did not.",
        "year_start": -3769,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 4:26, Genesis 5:6",
        "key_actors": ["Seth", "Enos"],
        "source_references": ["Ussher Annals 235d AM, 945 JP"],
        "extra_data": {
            "annals_reference": "235d AM, 945 JP",
            "significance": "corruption_of_worship_begins",
            "seth_age": 105
        }
    },
    
    # ANTEDILUVIAN PATRIARCHS
    {
        "name": "Birth of Cainan",
        "description": "Enos was 90 years old when Cainan was born",
        "year_start": -3679,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:9",
        "key_actors": ["Enos", "Cainan"],
        "source_references": ["Ussher Annals 325d AM, 1035 JP"],
        "extra_data": {"annals_reference": "325d AM, 1035 JP", "enos_age": 90}
    },
    {
        "name": "Birth of Mahalaleel",
        "description": "Cainan was 70 years old when Mahalaleel was born",
        "year_start": -3609,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:12",
        "key_actors": ["Cainan", "Mahalaleel"],
        "source_references": ["Ussher Annals 395d AM, 1105 JP"],
        "extra_data": {"annals_reference": "395d AM, 1105 JP", "cainan_age": 70}
    },
    {
        "name": "Birth of Jared",
        "description": "Mahalaleel was 65 years old when Jared was born",
        "year_start": -3544,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:15",
        "key_actors": ["Mahalaleel", "Jared"],
        "source_references": ["Ussher Annals 460d AM, 1170 JP"],
        "extra_data": {"annals_reference": "460d AM, 1170 JP", "mahalaleel_age": 65}
    },
    {
        "name": "Birth of Enoch",
        "description": "Jared was 162 years old when Enoch was born",
        "year_start": -3382,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:18",
        "key_actors": ["Jared", "Enoch"],
        "source_references": ["Ussher Annals 622d AM, 1332 JP"],
        "extra_data": {"annals_reference": "622d AM, 1332 JP", "jared_age": 162}
    },
    {
        "name": "Birth of Methuselah",
        "description": "Enoch was 65 years old when Methuselah was born. Methuselah would become the longest-lived human in recorded history.",
        "year_start": -3317,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:21",
        "key_actors": ["Enoch", "Methuselah"],
        "source_references": ["Ussher Annals 687d AM, 1397 JP"],
        "extra_data": {
            "annals_reference": "687d AM, 1397 JP",
            "enoch_age": 65,
            "significance": "longest_lived_human"
        }
    },
    {
        "name": "Birth of Lamech",
        "description": "Methuselah was 187 years old when Lamech was born",
        "year_start": -3130,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:25",
        "key_actors": ["Methuselah", "Lamech"],
        "source_references": ["Ussher Annals 874d AM, 1584 JP"],
        "extra_data": {"annals_reference": "874d AM, 1584 JP", "methuselah_age": 187}
    },
    {
        "name": "Death of Adam",
        "description": "Adam died at age 930, having seen nine generations of his descendants",
        "year_start": -3074,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:5",
        "key_actors": ["Adam"],
        "source_references": ["Ussher Annals 930d AM, 1640 JP"],
        "extra_data": {
            "annals_reference": "930d AM, 1640 JP",
            "age_at_death": 930,
            "significance": "first_human_death_from_old_age"
        }
    },
    {
        "name": "Translation of Enoch",
        "description": "Enoch walked with God and was translated without seeing death at age 365. God took him because he pleased God through faith.",
        "year_start": -3017,
        "era": "creation_to_flood",
        "event_type": "religious",
        "biblical_source": "Genesis 5:22-24, Hebrews 11:5",
        "key_actors": ["Enoch", "God"],
        "source_references": ["Ussher Annals 987d AM, 1697 JP"],
        "extra_data": {
            "annals_reference": "987d AM, 1697 JP",
            "age_at_translation": 365,
            "significance": "first_translation_without_death",
            "pattern": "faith_overcomes_death"
        }
    },
    {
        "name": "Birth of Noah",
        "description": "Lamech was 182 years old when Noah was born. Lamech prophetically named him Noah saying 'This one will comfort us concerning our work and the toil of our hands, because of the ground which the LORD has cursed.'",
        "year_start": -2948,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:28-29",
        "key_actors": ["Lamech", "Noah"],
        "source_references": ["Ussher Annals 1056d AM, 1766 JP"],
        "extra_data": {
            "annals_reference": "1056d AM, 1766 JP",
            "lamech_age": 182,
            "significance": "birth_of_flood_survivor",
            "prophetic_naming": True
        }
    },
    {
        "name": "Birth of Shem, Ham, and Japheth",
        "description": "Noah was 500 years old when he begat Shem, Ham, and Japheth",
        "year_start": -2448,
        "era": "creation_to_flood",
        "event_type": "social",
        "biblical_source": "Genesis 5:32",
        "key_actors": ["Noah", "Shem", "Ham", "Japheth"],
        "source_references": ["Ussher Annals 1556d AM"],
        "extra_data": {"noah_age": 500}
    },

    # THE GREAT FLOOD
    {
        "name": "The Great Flood Begins",
        "description": "In the 600th year of Noah's life, in the second month, on the 17th day, all fountains of the great deep burst open and windows of heaven opened. God brought the flood to destroy all flesh in which was the breath of life because the earth was filled with violence. Noah, his family (8 people total), and animals entered the ark which God had commanded him to build.",
        "year_start": -2348,
        "era": "creation_to_flood",
        "event_type": "natural",
        "biblical_source": "Genesis 6:5-7:24",
        "key_actors": ["God", "Noah", "Noah's family"],
        "source_references": ["Ussher Annals 1656a AM, 2365 JP"],
        "extra_data": {
            "annals_reference": "1656a AM, 2365 JP",
            "noah_age": 600,
            "duration_days": 150,
            "significance": "global_judgment",
            "pattern": "judgment_on_violence_wickedness",
            "survivors": 8
        }
    },
    {
        "name": "Flood Waters Recede",
        "description": "After 150 days, the waters decreased. On the 17th day of the seventh month, the ark rested on Mount Ararat. On the first day of the tenth month, mountain tops became visible.",
        "year_start": -2348,
        "year_end": -2347,
        "era": "flood_to_abraham",
        "event_type": "natural",
        "biblical_source": "Genesis 8:1-5",
        "key_actors": ["Noah"],
        "source_references": ["Ussher Annals 1656-1657 AM"],
        "extra_data": {"significance": "flood_recession"}
    },
    {
        "name": "Noah Leaves the Ark",
        "description": "On the 27th day of the second month in Noah's 601st year, the earth was completely dry. God commanded Noah to leave the ark with all living creatures. Noah built an altar and offered burnt offerings. God blessed Noah and his sons, established the covenant with the rainbow sign, and gave permission to eat meat. God commanded: 'Be fruitful and multiply, and fill the earth.'",
        "year_start": -2347,
        "era": "flood_to_abraham",
        "event_type": "religious",
        "biblical_source": "Genesis 8:14-9:17",
        "key_actors": ["God", "Noah", "Shem", "Ham", "Japheth"],
        "source_references": ["Ussher Annals 1657a AM, 2366 JP"],
        "extra_data": {
            "annals_reference": "1657a AM, 2366 JP",
            "covenant": "Noahic_covenant",
            "rainbow_sign": True,
            "dietary_change": "meat_permitted",
            "significance": "new_beginning_for_humanity"
        }
    },

    # POST-FLOOD TO ABRAHAM
    {
        "name": "Tower of Babel",
        "description": "All earth had one language. Men settled in the land of Shinar and began building a city and tower reaching to heaven to make a name for themselves. God confused their language so they could not understand one another and scattered them over the face of all the earth. The city was called Babel because there God confused the language of all the earth.",
        "year_start": -2247,
        "year_start_min": -2350,
        "year_start_max": -2200,
        "era": "flood_to_abraham",
        "event_type": "social",
        "biblical_source": "Genesis 11:1-9",
        "key_actors": ["Humanity", "God"],
        "source_references": ["Ussher Annals ~1757d AM, 2467 JP"],
        "extra_data": {
            "annals_reference": "1757d AM, 2467 JP",
            "pattern": "pride_judgment_dispersion",
            "significance": "origin_of_languages_nations",
            "confidence": "medium"
        }
    },
    {
        "name": "Birth of Abraham (Abram)",
        "description": "Terah was 70 years old when he begat Abram, Nahor, and Haran. Abram would become the father of nations through whom God's covenant promises would flow.",
        "year_start": -2008,
        "era": "patriarchs",
        "event_type": "social",
        "biblical_source": "Genesis 11:26",
        "key_actors": ["Terah", "Abraham"],
        "source_references": ["Ussher Annals 1996d AM, 2706 JP"],
        "extra_data": {
            "annals_reference": "1996d AM, 2706 JP",
            "terah_age": 70,
            "significance": "birth_of_patriarch"
        }
    },
    {
        "name": "God's Call of Abraham",
        "description": "God called Abram to leave his country and kindred for a land God would show him. God promised: 'I will make you a great nation, bless you, make your name great. You will be a blessing. I will bless those who bless you and curse those who curse you. In you all families of the earth shall be blessed.' Abram was 75 years old when he departed from Haran with Sarai his wife and Lot his nephew.",
        "year_start": -1921,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 12:1-5, Acts 7:2-4",
        "key_actors": ["God", "Abraham", "Sarah", "Lot"],
        "source_references": ["Ussher Annals 2083a AM, 2792 JP"],
        "extra_data": {
            "annals_reference": "2083 AM, 2793 JP",
            "abram_age": 75,
            "covenant": "Abrahamic_covenant_initiated",
            "significance": "beginning_of_chosen_nation",
            "pattern": "faith_obedience_promise"
        }
    },
    {
        "name": "Abram Enters Canaan",
        "description": "Abram passed through the land to Shechem, to the terebinth tree of Moreh. The Canaanites were then in the land. The LORD appeared to Abram and said, 'To your descendants I will give this land.' Abram built an altar there to the LORD.",
        "year_start": -1921,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 12:6-7",
        "key_actors": ["God", "Abraham"],
        "source_references": ["Ussher Annals 2083 AM"],
        "extra_data": {"land_promise": "Canaan_promised_to_descendants"}
    },
    {
        "name": "Covenant Ceremony with Abraham",
        "description": "God made a formal covenant with Abram. A smoking oven and burning torch passed between the divided pieces. God said: 'To your descendants I have given this land, from the river of Egypt to the great river Euphrates.'",
        "year_start": -1911,
        "year_start_min": -1920,
        "year_start_max": -1910,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 15:1-21",
        "key_actors": ["God", "Abraham"],
        "source_references": ["Ussher Annals 2093 AM, 2803 JP"],
        "extra_data": {
            "annals_reference": "2093 AM, 2803 JP",
            "covenant": "Abrahamic_covenant_ratified",
            "land_boundaries": "Egypt_to_Euphrates",
            "prophesy": "400_years_Egyptian_bondage_predicted"
        }
    },
    {
        "name": "Birth of Ishmael",
        "description": "Sarai gave her maid Hagar to Abram as wife. Hagar conceived and bore Ishmael when Abram was 86 years old.",
        "year_start": -1911,
        "era": "patriarchs",
        "event_type": "social",
        "biblical_source": "Genesis 16:1-16",
        "key_actors": ["Abraham", "Hagar", "Ishmael"],
        "source_references": ["Ussher Annals 2092-2093 AM"],
        "extra_data": {"abram_age": 86}
    },
    {
        "name": "Covenant of Circumcision",
        "description": "When Abram was 99 years old, God appeared and established circumcision as the sign of the covenant. God changed Abram's name to Abraham ('father of many nations') and Sarai to Sarah. God promised Sarah would bear a son named Isaac through whom the covenant would be established. Abraham, Ishmael (13), and all males in Abraham's household were circumcised that same day.",
        "year_start": -1897,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 17:1-27",
        "key_actors": ["God", "Abraham", "Sarah"],
        "source_references": ["Ussher Annals 2107 AM"],
        "extra_data": {
            "abraham_age": 99,
            "covenant_sign": "circumcision",
            "name_change": {"Abram": "Abraham", "Sarai": "Sarah"},
            "promise": "Isaac_promised"
        }
    },
    {
        "name": "Destruction of Sodom and Gomorrah",
        "description": "God revealed to Abraham His plan to destroy Sodom and Gomorrah for their great wickedness. Abraham interceded for the righteous. Angels rescued Lot and his family from Sodom. God rained brimstone and fire from heaven, destroying Sodom, Gomorrah, and all the plain. Lot's wife became a pillar of salt when she looked back.",
        "year_start": -1897,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 18:16-19:29",
        "key_actors": ["God", "Abraham", "Lot", "Angels"],
        "source_references": ["Ussher Annals 2107-2108 AM"],
        "extra_data": {
            "pattern": "judgment_on_sexual_immorality",
            "intercession": "Abraham_pleaded_for_righteous",
            "destruction_method": "fire_and_brimstone",
            "significance": "eternal_warning"
        }
    },
    {
        "name": "Birth of Isaac",
        "description": "Sarah conceived and bore Abraham a son in his old age, at the appointed time God had spoken. Abraham was 100 years old when Isaac was born. Abraham circumcised Isaac on the eighth day. God's promise of a son through Sarah was fulfilled.",
        "year_start": -1896,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 21:1-7",
        "key_actors": ["Abraham", "Sarah", "Isaac"],
        "source_references": ["Ussher Annals 2108 AM"],
        "extra_data": {
            "abraham_age": 100,
            "sarah_age": 90,
            "significance": "miracle_birth_covenant_heir",
            "pattern": "promise_fulfilled"
        }
    },
    {
        "name": "Binding of Isaac (Akedah)",
        "description": "God tested Abraham, commanding him to offer Isaac as a burnt offering on Mount Moriah. Abraham obeyed, building an altar and binding Isaac. As Abraham stretched out his hand with the knife, the Angel of the LORD stopped him. God provided a ram caught in a thicket as a substitute sacrifice. God reaffirmed the covenant: 'In your seed all nations of the earth shall be blessed, because you have obeyed My voice.'",
        "year_start": -1872,
        "year_start_min": -1880,
        "year_start_max": -1860,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 22:1-19",
        "key_actors": ["God", "Abraham", "Isaac", "Angel of the LORD"],
        "source_references": ["Ussher Annals ~2132 AM"],
        "extra_data": {
            "location": "Mount_Moriah",
            "pattern": "substitutionary_sacrifice_foreshadowing_Christ",
            "significance": "supreme_test_of_faith",
            "covenant_reaffirmed": True,
            "messianic_promise": "in_your_seed_all_nations_blessed"
        }
    },
    {
        "name": "Death of Sarah",
        "description": "Sarah died at age 127 in Kirjath Arba (Hebron) in the land of Canaan. Abraham mourned and wept for Sarah. He purchased the cave of Machpelah from Ephron the Hittite as a burial place, paying 400 shekels of silver. Sarah was buried in the cave of the field of Machpelah.",
        "year_start": -1860,
        "era": "patriarchs",
        "event_type": "social",
        "biblical_source": "Genesis 23:1-20",
        "key_actors": ["Sarah", "Abraham", "Ephron"],
        "source_references": ["Ussher Annals 2144 AM"],
        "extra_data": {
            "sarah_age": 127,
            "burial_place": "Cave_of_Machpelah_Hebron",
            "property_purchase": "first_owned_land_in_Canaan",
            "significance": "matriarch_of_faith"
        }
    },
    {
        "name": "Marriage of Isaac and Rebekah",
        "description": "Abraham sent his eldest servant to Mesopotamia to find a wife for Isaac from his own kindred. The servant prayed for a sign, and Rebekah fulfilled it at the well. She was the daughter of Bethuel, granddaughter of Nahor (Abraham's brother). Isaac was 40 years old when he married Rebekah.",
        "year_start": -1856,
        "era": "patriarchs",
        "event_type": "social",
        "biblical_source": "Genesis 24:1-67, Genesis 25:20",
        "key_actors": ["Abraham", "Isaac", "Rebekah", "Abraham's servant"],
        "source_references": ["Ussher Annals 2148 AM"],
        "extra_data": {
            "isaac_age": 40,
            "significance": "covenant_line_continued",
            "divine_guidance": "servant's_prayer_answered"
        }
    },
    {
        "name": "Death of Abraham",
        "description": "Abraham died at age 175 in a good old age, an old man and full of years, and was gathered to his people. Isaac and Ishmael buried him in the cave of Machpelah with Sarah his wife.",
        "year_start": -1821,
        "era": "patriarchs",
        "event_type": "social",
        "biblical_source": "Genesis 25:7-10",
        "key_actors": ["Abraham", "Isaac", "Ishmael"],
        "source_references": ["Ussher Annals 2183 AM"],
        "extra_data": {
            "age_at_death": 175,
            "burial_place": "Cave_of_Machpelah",
            "significance": "father_of_faith_patriarch_of_Israel",
            "pattern": "promise_fulfilled_died_in_faith"
        }
    },
    {
        "name": "Birth of Esau and Jacob",
        "description": "Isaac was 60 years old when Rebekah bore twins. The first came out red and hairy, named Esau. His brother came out with his hand holding Esau's heel, named Jacob. God told Rebekah before their birth: 'Two nations are in your womb, two peoples shall be separated; one shall be stronger, the older shall serve the younger.'",
        "year_start": -1836,
        "era": "patriarchs",
        "event_type": "social",
        "biblical_source": "Genesis 25:21-26",
        "key_actors": ["Isaac", "Rebekah", "Esau", "Jacob"],
        "source_references": ["Ussher Annals 2168 AM"],
        "extra_data": {
            "isaac_age": 60,
            "prophetic_word": "older_will_serve_younger",
            "significance": "covenant_line_determined_before_birth",
            "pattern": "sovereign_election"
        }
    },
    {
        "name": "Esau Sells His Birthright",
        "description": "Esau came in from the field exhausted and demanded Jacob's red stew. Jacob said, 'Sell me your birthright.' Esau despised his birthright and sold it for a meal. Thus Esau despised his birthright.",
        "year_start": -1800,
        "year_start_min": -1820,
        "year_start_max": -1780,
        "era": "patriarchs",
        "event_type": "social",
        "biblical_source": "Genesis 25:29-34, Hebrews 12:16",
        "key_actors": ["Esau", "Jacob"],
        "source_references": ["Ussher Annals AM ~2200"],
        "extra_data": {
            "pattern": "despising_spiritual_for_temporal",
            "significance": "birthright_transferred_to_Jacob",
            "warning": "profane_person_Esau"
        }
    },
    {
        "name": "Jacob Receives Isaac's Blessing",
        "description": "When Isaac was old and his eyes dim, Rebekah helped Jacob deceive Isaac to receive the firstborn's blessing intended for Esau. Isaac blessed Jacob with dew of heaven, fatness of earth, abundance of grain and wine, dominion over peoples, and pronounced: 'Cursed be everyone who curses you, and blessed be those who bless you!' When Esau returned, Isaac could not retract the blessing but gave Esau a lesser blessing.",
        "year_start": -1760,
        "year_start_min": -1780,
        "year_start_max": -1740,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 27:1-40",
        "key_actors": ["Isaac", "Rebekah", "Jacob", "Esau"],
        "source_references": ["Ussher Annals AM ~2244"],
        "extra_data": {
            "deception": "Jacob_disguised_as_Esau",
            "blessing": "covenant_blessing_transferred",
            "consequence": "Esau_hatred_Jacob_flees",
            "significance": "sovereign_purpose_through_human_weakness"
        }
    },
    {
        "name": "Jacob's Ladder Vision at Bethel",
        "description": "Jacob fled from Esau toward Haran. At a certain place he slept with a stone for a pillow. He dreamed of a ladder set up on earth reaching to heaven with angels ascending and descending. The LORD stood above it and confirmed the Abrahamic covenant: 'The land on which you lie I give to you and your descendants. Your descendants shall be as the dust of the earth, spreading abroad. In you and your seed all families of the earth shall be blessed. I am with you and will keep you wherever you go.' Jacob awoke in fear, saying, 'This is the house of God and gate of heaven!' He named the place Bethel and vowed to give God a tenth of all.",
        "year_start": -1760,
        "era": "patriarchs",
        "event_type": "religious",
        "biblical_source": "Genesis 28:10-22",
        "key_actors": ["God", "Jacob", "Angels"],
        "source_references": ["Ussher Annals 2244-2245 AM"],
        "extra_data": {
            "location": "Bethel",
            "vision": "ladder_to_heaven_angels",
            "covenant_confirmed": "Abrahamic_covenant_to_Jacob",
            "vow": "tithe_promised",
            "significance": "Christ_the_ladder_John_1:51"
        }
    },
]
