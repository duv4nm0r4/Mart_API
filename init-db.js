db = db.getSiblingDB("mart_db");
db.word_lists.drop();
db.word_lists.insert(
    {
        "URL_search": {
            "google": {
                "CaesarEncryption_word": "tbbtyr",
                "length_word": 6,
                "letters_used_word_count": {
                    "e": 1,
                    "g": 2,
                    "l": 1,
                    "o": 2
                },
                "longest_word": "google",
                "lowercase_count": 6,
                "uppercase_count": 0
            }
        },
        "list_words": [
            "12345",
            "Smart",
            "https://www.google.com"
        ],
        "long_words": {
            "https://www.google.com": {
                "CaesarEncryption_word": "uggcf://jjj.tbbtyr.pbz",
                "length_word": 22,
                "letters_used_word_count": {
                    ".": 2,
                    "/": 2,
                    ":": 1,
                    "c": 1,
                    "e": 1,
                    "g": 2,
                    "h": 1,
                    "l": 1,
                    "m": 1,
                    "o": 3,
                    "p": 1,
                    "s": 1,
                    "t": 2,
                    "w": 3
                },
                "longest_word": "https://www.google.com",
                "lowercase_count": 22,
                "uppercase_count": 0
            }
        },
        "mart_search": [
            "Smart"
        ]
    }
);