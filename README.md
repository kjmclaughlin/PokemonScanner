# PokemonScanner

Pokemon Scanner is an application that scans the coordinates determined in the scan script itself for pokemon entered in desiredPokemon.txt and then sends email notifications to the people listed in the passed in emaillist with a link to the given pokemon's location in google maps.  This allows the user to quickly locate pokemon in their area which they actually carry about ( not Zubats ).  

This application uses the data API of pokevision.com so credit to them for giving access to pokemon in a location so conveniently.  

For anyone interested in using this for themself.  Take scanScript.py and change the lat and long at the top to coordinates that you care about.  Then create a gmail that you have access to for the emailer.  Enter the gmail account name under message from and then create a file called GmailLogin.txt and put in your password as the single line.  Then create an email list for the people to receive the emails, one per line.  Then you can add or subtract from desiredPokemon.txt as you want to get the correct list.  LEAVE pokemonList.txt ALONE OR YOU WILL GET INCORRECT TRACKING.  Feel free to do with this what you please.
