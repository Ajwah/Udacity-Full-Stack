import media

toy_Story = media.Movie("Toy Story",
                        "Toy comes to live",
                        "http://www.gstatic.com/tv/thumb/movieposters/17420/p17420_p_v7_aa.jpg",
                        "https://youtu.be/vwyZH85NQC4")
avatar = media.Movie("Avatar",
                     "A marine on an alien planet",
                     "http://t0.gstatic.com/images?q=tbn:ANd9GcQCfmvrE4fMo2cd8esc7mDZPtFSJThAujddMPkRtti1_ij6u-jp",
                     "https://www.youtube.com/watch?v=cRdxXPV9GNQ")

print(avatar.storyline)
avatar.showtrailer()
