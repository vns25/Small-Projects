
var rl = require('readline'); 
var prompt = rl.createInterface(process.stdin, process.stdout )
function randomNumber(range) 
{  
    return Math.floor( Math.random() * range) + 1; 
}  

var wins = 0; 
var rounds = 0; 
function play()
{
    prompt.question("Enter 1 for Rock, 2 for Paper, 3 for Scissors. \n", function(input) 
    {
        rounds++; 
        var com = randomNumber(3); 
        console.log("Computer chooses: " + com); 
        while(true)
        {
            if(input == com)
            {
                if(input == 1)
                {
                    console.log("Rock vs Rock! It's a tie. "); 
                    break; 
                }
                else if(input == 2 )
                {
                    console.log("Paper vs Paper! It's a tie. ")
                    break; 
                }
                else if(input == 3 )
                {
                    console.log("Scissors vs Scissors! It's a tie. ")
                    break; 
                } 
            }
            else if(input == 1)
            {
                if(com == 2)
                {
                    console.log("Rock vs Paper! You lose :( ");
                    break; 
                }
                else if(com == 3) 
                {
                    console.log("Rock vs Scissors! You win! "); 
                    wins++; 
                    break; 
                }
            }
            else if(input == 2)
            {
                if(com == 1)
                {
                    console.log("Paper vs Rock! You win! "); 
                    wins++; 
                    break; 
                }
                else if(com == 3) 
                {
                    console.log("Paper vs Scissors! You lose "); 
                    break; 
                }
            }

            else
            {
                if(com == 1)
                {
                    console.log("Scissors vs Rock! You lose :( "); 
                    break; 
                }
                else if(com == 2) 
                {
                    console.log("Paper vs Scissors! You win! :("); 
                    wins++; 
                    break; 
                }
            }

        } 
        prompt.question("Play again? Enter Y or N: \n", function(anotherRound) 
            {
                if(anotherRound == "Y")
                {
                    play(); 
                }
                else 
                {
                   console.log("Wins: " + wins + "/" + rounds); 
                }
            }); 
    }); 
}

play(); 