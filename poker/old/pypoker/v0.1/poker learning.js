// JavaScript Learning Guide
// Let's start with the basics and work our way up!

console.log("Welcome to JavaScript Learning!");

// ========================
// 1. VARIABLES & DATA TYPES
// ========================

// Variables - ways to store data
let playerName = "Alice";           // String (text)
let playerAge = 25;                 // Number
let isActive = true;                // Boolean (true/false)
let cards = null;                   // Null (intentionally empty)
let score;                          // Undefined (declared but no value)

// Constants - values that don't change
const DECK_SIZE = 52;
const GAME_NAME = "Poker";

console.log("Player:", playerName, "Age:", playerAge);

// ========================
// 2. ARRAYS (Lists of data)
// ========================

// Creating arrays
let suits = ["Hearts", "Diamonds", "Clubs", "Spades"];
let numbers = [1, 2, 3, 4, 5];
let mixed = ["Alice", 25, true, null];

// Array methods
console.log("First suit:", suits[0]);           // Access first item
console.log("Array length:", suits.length);     // Get length
suits.push("Joker");                            // Add to end
console.log("After adding:", suits);

// ========================
// 3. OBJECTS (Groups of related data)
// ========================

// Creating an object
let player = {
    name: "Bob",
    chips: 1000,
    hand: ["Ace of Spades", "King of Hearts"],
    isDealer: false,
    
    // Objects can have functions (methods)
    showHand: function() {
        console.log(this.name + "'s hand:", this.hand);
    }
};

// Accessing object properties
console.log("Player name:", player.name);
console.log("Player chips:", player.chips);
player.showHand();

// ========================
// 4. FUNCTIONS (Reusable code blocks)
// ========================

// Function declaration
function greetPlayer(name) {
    return "Hello, " + name + "! Welcome to the game!";
}

// Function with multiple parameters
function calculateWinnings(bet, multiplier) {
    return bet * multiplier;
}

// Arrow function (modern syntax)
const dealCard = () => {
    const suits = ["♠", "♥", "♦", "♣"];
    const values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
    
    const randomSuit = suits[Math.floor(Math.random() * suits.length)];
    const randomValue = values[Math.floor(Math.random() * values.length)];
    
    return randomValue + randomSuit;
};

// Using functions
console.log(greetPlayer("Charlie"));
console.log("Winnings:", calculateWinnings(100, 2));
console.log("Random card:", dealCard());

// ========================
// 5. CONDITIONALS (Making decisions)
// ========================

let playerScore = 85;

if (playerScore >= 90) {
    console.log("Excellent play!");
} else if (playerScore >= 70) {
    console.log("Good job!");
} else {
    console.log("Keep practicing!");
}

// Ternary operator (shorthand if/else)
let status = playerScore >= 70 ? "Winner" : "Try again";
console.log("Status:", status);

// ========================
// 6. LOOPS (Repeating actions)
// ========================

// For loop - repeat a specific number of times
console.log("\nDealing 5 cards:");
for (let i = 0; i < 5; i++) {
    console.log("Card " + (i + 1) + ":", dealCard());
}

// While loop - repeat while condition is true
let gameChips = 100;
let round = 1;

while (gameChips > 0 && round <= 3) {
    console.log(`Round ${round}: You have ${gameChips} chips`);
    gameChips -= 20; // Simulate betting
    round++;
}

// For...of loop - iterate through arrays
console.log("\nAll suits:");
for (let suit of suits) {
    console.log("Suit:", suit);
}

// ========================
// 7. PRACTICAL EXAMPLE: Simple Poker Hand Evaluator
// ========================

function createPokerHand() {
    let hand = [];
    for (let i = 0; i < 5; i++) {
        hand.push(dealCard());
    }
    return hand;
}

function evaluateHand(hand) {
    console.log("Your hand:", hand.join(", "));
    
    // Simple evaluation - check for pairs
    let values = hand.map(card => card.slice(0, -1)); // Remove suit
    let valueCounts = {};
    
    // Count each value
    for (let value of values) {
        valueCounts[value] = (valueCounts[value] || 0) + 1;
    }
    
    // Check for pairs
    let pairs = Object.values(valueCounts).filter(count => count === 2);
    let threeOfAKind = Object.values(valueCounts).some(count => count === 3);
    let fourOfAKind = Object.values(valueCounts).some(count => count === 4);
    
    if (fourOfAKind) {
        return "Four of a Kind!";
    } else if (threeOfAKind) {
        return "Three of a Kind!";
    } else if (pairs.length === 2) {
        return "Two Pair!";
    } else if (pairs.length === 1) {
        return "One Pair!";
    } else {
        return "High Card";
    }
}

// Let's play!
console.log("\n=== POKER HAND DEMO ===");
let myHand = createPokerHand();
let result = evaluateHand(myHand);
console.log("Result:", result);

// ========================
// 8. MODERN JAVASCRIPT FEATURES
// ========================

// Template literals (using backticks)
let playerInfo = `Player ${player.name} has ${player.chips} chips`;
console.log(playerInfo);

// Destructuring - extract values from objects/arrays
let {name: playerNameFromObj, chips: playerChips} = player;
console.log(`Destructured: ${playerNameFromObj} has ${playerChips} chips`);

let [firstSuit, secondSuit] = suits;
console.log("First two suits:", firstSuit, secondSuit);

// Spread operator - expand arrays/objects
let newHand = [...myHand, dealCard()]; // Add a card to hand
console.log("Extended hand:", newHand);

// ========================
// EXERCISES FOR YOU TO TRY:
// ========================

/*
1. Create a function that calculates the total value of a poker hand
   (Ace=1, Jack=11, Queen=12, King=13, numbers=face value)

2. Make a function that shuffles an array (deck of cards)

3. Create a simple betting system where players can bet chips

4. Try to detect a flush (all same suit) in a poker hand

5. Build a simple card game like "Higher or Lower"

Remember:
- Use console.log() to see what your code is doing
- Test small pieces of code before building bigger features
- Don't be afraid to experiment!
- Check the browser's developer console for any error messages
*/

console.log("\n=== Ready to start coding! ===");
console.log("Try modifying this code or adding your own functions!");