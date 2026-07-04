# Scholastic Battle Arenas & Questions Data

DUEL_ARENAS = {
    "1": "Speed Aptitude Arena (Quant shortcuts for CGL/CDS)",
    "2": "UPSC Concept Clash (Deep GS assertions)",
    "3": "Spelling Bee / Grammar Lab (Pinpoint syntax/orthography)"
}

DUEL_QUESTIONS = {
    "1": [
        {
            "question": "What is the unit digit of 27^23 * 34^38 * 53^47?",
            "options": ["A. 2", "B. 6", "C. 8", "D. 4"],
            "correct": "B",
            "explanation": "Unit digit calculations:\n- 27^23: 7^23. Cyclicity of 7 is 4. 23 mod 4 = 3. 7^3 ends in 3.\n- 34^38: 4^38. 4^even ends in 6.\n- 53^47: 3^47. Cyclicity of 3 is 4. 47 mod 4 = 3. 3^3 ends in 7.\nMultiplication: 3 * 6 * 7 = 126, which ends in 6. Correct option is B."
        },
        {
            "question": "Pipe A fills a cistern in 12 min and Pipe B fills it in 15 min. Pipe C empties it in 6 min. If A and B are open for 5 min initially and then C is also opened, how long does it take to empty the cistern?",
            "options": ["A. 30 min", "B. 45 min", "C. 37.5 min", "D. 15 min"],
            "correct": "B",
            "explanation": "Let total capacity = 60 units (LCM of 12, 15, 6).\n- Efficiency of A = +5, B = +4, C = -10.\n- Combined A+B = +9. In 5 min, they fill 9 * 5 = 45 units.\n- When C opens, net efficiency = 5 + 4 - 10 = -1 unit/min.\n- Time to empty filled 45 units = 45 / 1 = 45 minutes. Correct option is B."
        },
        {
            "question": "If the difference between CI and SI on a sum for 3 years at 10% p.a. is Rs. 93, what is the principal sum?",
            "options": ["A. Rs. 3000", "B. Rs. 4000", "C. Rs. 2500", "D. Rs. 3500"],
            "correct": "A",
            "explanation": "Formula for difference for 3 years: Diff = P * (r/100)^2 * (3 + r/100).\nHere, 93 = P * (1/10)^2 * (3 + 0.1) = P * (1/100) * 3.1.\n93 = P * 0.031 => P = 93 / 0.031 = Rs. 3000. Correct option is A."
        },
        {
            "question": "A train crosses a platform 100 m long in 60 seconds at a speed of 45 km/h. What is the time taken by the train to cross an electric pole?",
            "options": ["A. 52 sec", "B. 60 sec", "C. 48 sec", "D. 44 sec"],
            "correct": "A",
            "explanation": "Speed = 45 * 5/18 = 12.5 m/s.\nPlatform cross: Length of train (T) + Platform (100) = Speed * Time = 12.5 * 60 = 750 m => T = 650 m.\nCrossing pole: Time = T / Speed = 650 / 12.5 = 52 seconds. Correct option is A."
        },
        {
            "question": "Find the value of sqrt(30 + sqrt(30 + sqrt(30 + ... to infinity))):",
            "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
            "correct": "B",
            "explanation": "Let x = sqrt(30 + x) => x^2 - x - 30 = 0 => (x - 6)(x + 5) = 0.\nSince the root value must be positive, x = 6. Correct option is B."
        }
    ],
    "2": [
        {
            "question": "Consider the following statements regarding the Attorney General of India:\n1. Must be qualified to be appointed as a Judge of the Supreme Court.\n2. Has the right of audience in all courts within the territory of India.\nWhich of the statements is/are correct?",
            "options": ["A. 1 only", "B. 2 only", "C. Both 1 and 2", "D. Neither 1 nor 2"],
            "correct": "C",
            "explanation": "Under Article 76, the AG must be qualified to be appointed a judge of the Supreme Court and has the right of audience in all courts in India. Both statements are correct. Correct option is C."
        },
        {
            "question": "Under the Constitution of India, which of the following is NOT a Fundamental Duty?",
            "options": ["A. To vote in public elections", "B. To develop scientific temper", "C. To safeguard public property", "D. To abide by the Constitution"],
            "correct": "A",
            "explanation": "Voting in public elections is a constitutional/legal right, not listed as a Fundamental Duty under Article 51A. Developing scientific temper, safeguarding public property, and abiding by the Constitution are Fundamental Duties. Correct option is A."
        },
        {
            "question": "Which of the following macroeconomic reports is NOT published by the World Bank Group?",
            "options": ["A. World Development Report", "B. Global Economic Prospects", "C. World Economic Outlook", "D. None of the above"],
            "correct": "C",
            "explanation": "The World Economic Outlook is published by the International Monetary Fund (IMF), not the World Bank. Correct option is C."
        },
        {
            "question": "With reference to the Indian Parliament, which of the following is correct regarding a Money Bill?",
            "options": ["A. It can be introduced in either House of Parliament", "B. Rajya Sabha has the power to reject or amend it", "C. The Speaker of Lok Sabha's decision on whether a bill is a Money Bill is final", "D. It requires recommendation of the Prime Minister"],
            "correct": "C",
            "explanation": "Under Article 110, if any question arises whether a Bill is a Money Bill or not, the decision of the Speaker of the House of the People (Lok Sabha) is final. It can only be introduced in Lok Sabha and requires President's recommendation. Correct option is C."
        },
        {
            "question": "The 42nd Amendment Act (1976) added which of the following Directive Principles (DPSPs)?\n1. Equal justice and free legal aid.\n2. Participation of workers in management of industries.\n3. Protection of environment and wild life.\nSelect the correct option:",
            "options": ["A. 1 and 2 only", "B. 2 and 3 only", "C. 1 and 3 only", "D. All of the above"],
            "correct": "D",
            "explanation": "The 42nd Amendment added Article 39A (Free Legal Aid), Article 43A (Participation of Workers), and Article 48A (Environment/Wildlife protection). Hence, all of the above are correct. Correct option is D."
        }
    ],
    "3": [
        {
            "question": "Identify the word with the correct spelling:",
            "options": ["A. Bureaucracy", "B. Bureacracy", "C. Burocracy", "D. Beauraucracy"],
            "correct": "A",
            "explanation": "The correct spelling is 'Bureaucracy'. Root syllables: Bu-reau-cra-cy. Correct option is A."
        },
        {
            "question": "Identify the grammatical error in: 'Neither of the systems work as expected.'",
            "options": ["A. Neither of", "B. the systems", "C. work", "D. as expected"],
            "correct": "C",
            "explanation": "The subject 'Neither' is singular, therefore it must take a singular verb: 'works', not 'work'. Correct option is C."
        },
        {
            "question": "Which of the following is the correct spelling?",
            "options": ["A. Accomodate", "B. Accommodate", "C. Acomodate", "D. Acommodate"],
            "correct": "B",
            "explanation": "The correct spelling is 'Accommodate' with double 'c' and double 'm'. Correct option is B."
        },
        {
            "question": "Fill in the blank: 'She is one of those officers who ___ always dedicated to their duty.'",
            "options": ["A. is", "B. are", "C. was", "D. has been"],
            "correct": "B",
            "explanation": "The relative pronoun 'who' refers to the plural antecedent 'officers', making the clause plural. Hence, it takes the plural verb 'are'. Correct option is B."
        },
        {
            "question": "Identify the misspelled word from the list:",
            "options": ["A. Occurrence", "B. Questionnaire", "C. Harass", "D. Embarass"],
            "correct": "D",
            "explanation": "The correct spelling is 'Embarrass' with double 'r'. Correct option is D."
        }
    ]
}
