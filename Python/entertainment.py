import media
import fresh_tomatoes

toy_Story = media.Movie("Toy Story",
                        "Toy comes to live",
                        "http://www.gstatic.com/tv/thumb/movieposters/17420/p17420_p_v7_aa.jpg",
                        "https://youtu.be/vwyZH85NQC4")
avatar = media.Movie("Avatar",
                     "A marine on an alien planet",
                     "http://t0.gstatic.com/images?q=tbn:ANd9GcQCfmvrE4fMo2cd8esc7mDZPtFSJThAujddMPkRtti1_ij6u-jp",
                     "https://www.youtube.com/watch?v=cRdxXPV9GNQ")
lord_rings = media.Movie("LOrd of the Rings", "Collecting rings",
                         "http://www.gstatic.com/tv/thumb/movieposters/28828/p28828_p_v7_aa.jpg",
                         "https://youtu.be/qyquczkXgPc")

shrek = media.Movie("Shrek", "Once upon a time, in a far away swamp, there lived an ogre named Shrek (Mike Myers) whose precious solitude is suddenly shattered by an invasion of annoying fairy tale characters. They were all banished from their kingdom by the evil Lord Farquaad (John Lithgow). Determined to save their home -- not to mention his -- Shrek cuts a deal with Farquaad and sets out to rescue Princess Fiona (Cameron Diaz) to be Farquaad's bride. Rescuing the Princess may be small compared to her deep, dark secret.",
                    "http://t2.gstatic.com/images?q=tbn:ANd9GcS_OkJKQ6ZpDV_xhC0L9zyHEcKMlV9x3Q30LF6MOE0nV1U6r09p",
                    "https://youtu.be/IlsMVMENn_0")

monsters_inc = media.Movie("Monsters, Inc.",
                           "Monsters Incorporated is the largest scare factory in the monster world, and James P. Sullivan (John Goodman) is one of its top scarers. Sullivan is a huge, intimidating monster with blue fur, large purple spots and horns. His scare assistant, best friend and roommate is Mike Wazowski (Billy Crystal), a green, opinionated, feisty little one-eyed monster. Visiting from the human world is Boo (Mary Gibbs), a tiny girl who goes where no human has ever gone before.",
                           "https://upload.wikimedia.org/wikipedia/en/6/63/Monsters_Inc.JPG",
                           "https://youtu.be/8IBNZ6O2kMk")

pearl_harbor = media.Movie("Pearl Harbor",
                           "This sweeping drama, based on real historical events, follows American boyhood friends Rafe McCawley (Ben Affleck) and Danny Walker (Josh Hartnett) as they enter World War II as pilots. Rafe is so eager to take part in the war that he departs to fight in Europe alongside England's Royal Air Force. On the home front, his girlfriend, Evelyn (Kate Beckinsale), finds comfort in the arms of Danny. The three of them reunite in Hawaii just before the Japanese attack on Pearl Harbor.",
                           "http://www.gstatic.com/tv/thumb/movieposters/27437/p27437_p_v7_aa.jpg",
                           "https://youtu.be/ozksd76CSIs")

movies = [toy_Story, avatar, lord_rings,shrek,monsters_inc,pearl_harbor]
fresh_tomatoes.open_movies_page(movies)
