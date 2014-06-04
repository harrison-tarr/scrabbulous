function hideOutputs() {
	output1 = document.getElementById("createWordsOutput");
	output2 = document.getElementById("checkWordsOutput");
	output1.style.display = "none"
	output2.style.display = "none"
}

function toggleInstructions() {

	instructionHolderBar = document.getElementById("instruction-menu");
	instructionToggler = document.getElementById("instruction-toggler");

	if (instructionHolderBar.lastChild.id != "instructions-verbose") {
		var instructions = document.createElement("div");
		instructions.id = "instructions-verbose";
		instructions.style.padding = "5px 0px 0px";
		instructions.style.positioning = "absolute";
		//instructions.style.zIndex = "100";
		instructions.innerText = "To create words, you have a couple options. You can type your letters, to generate words based on just your letters. You can "+
		"also type a word from the board after your letters to use as a cross-word. e.g. 'ieslfn hello' which produces a bunch of words, including 'elfish' which uses the 'h' from 'hello "+
		"Alternately, you can put a second word with a dash, as a suffix, prefix, or infix for your word. e.g. 'fast -ing' produces a bunch of words, including 'fasting' which uses the 'fast' and 'ing' as a suffix "+
		"e.g. 'fix pre-' produces a bunch of words, including 'prefix', which uses the 'pre' as a prefix, and fills in the rest with 'fix'";
		instructionToggler.innerHTML = '<img src="./static/downarrow.png" style="display: inline; height: .75em" /> Click here to hide.';
		instructionHolderBar.appendChild(instructions);
		
	}
	else {
		instructionHolderBar.removeChild(document.getElementById("instructions-verbose"));
		instructionToggler.innerHTML = '<img src="./static/rightarrow.png" style="display: inline; height: .75em" /> Click here for instructions.';

	}
}

function addSearch(searchText) {
	historyHandler = document.getElementById("history-handler");
	var newSearch = document.createElement("div");
	newSearch.style.padding = "5px .5em 5px";
	newSearch.innerHTML = searchText;
	historyHandler.insertBefore(newSearch, historyHandler.firstChild);
	if (historyHandler.children.length > 15) {
		historyHandler.removeChild(historyHandler.lastChild);
	}
}
function calculateScore(answers) {
	var scores = {};
	var letter_value_global = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o":1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10 };
	for (var i = 0; i < answers.length; i++) {
		console.log(answers[i]);
		var wordScore = 0;
		for (var j = 0; j < answers[i].length; j++) {
			wordScore += letter_value_global[answers[i][j]];
		}
		scores[answers[i]] = wordScore;
	}
	return scores;
}

function findMaxScore(scores) {
	var maxScore = 0;
	var highWord = "";
	for (key in scores) {
		if (scores[key] > maxScore) {
			maxScore = scores[key];
			highWord = key;
		}
	}
	return highWord + "-" + maxScore
}

function unicodeArrayToStringArray(answers) {
	var answers = answers.substring(1, answers.length-1);
	answers = answers.split(",");
	console.log(answers);
	stringArray = [];
	for (var i = 0; i < answers.length; i++) {
		console.log(i);
		answers[i] = answers[i].trim();
		stringArray.push(String(answers[i].substring(2, answers[i].length-1)));
	}
	return stringArray;
}

function printFormattedCalculated(answers) {
	console.log("Beginning print");
	var printableString = "";
	var length = 0;
	var count = 0;
	words_and_scores = calculateScore(answers);
	console.log("Finished Calculating");
	console.log(answers.length);
	for (var i = 0; i < answers.length; i++) {
		if (printableString == "") {
			printableString += String(answers[i].length) + ":<br />";
			length = answers[i].length;
			count = 0;
		}
		else if (answers[i].length != length) {
			printableString += "<br /><br />"+String(answers[i].length) + ":<br />";
			length = answers[i].length;
			count = 0;
		}
		if (count == 7) {
			printableString += "<br />"; 
			count = 0;
		}
		count+=1;
		printableString +=  String(answers[i]) + "-" + String(words_and_scores[answers[i]]) + "&emsp;&emsp;";
	}
	printableString += "<br />";
	if (answers == []) {
		printableString =  "No answers found!";
			return printableString;
	}
	printableString = "HighScore = " + findMaxScore(words_and_scores) + "<br /><br />" + printableString;
	var highScoreReturn = findMaxScore(words_and_scores);
	console.log("Ending print");
	return [printableString, highScoreReturn];
}


function createWords() {
	hideOutputs();
	var output = document.getElementById("createWordsOutput");
	output.style.textAlign = "left";
	//output.style.display = "none"
	var input = document.getElementById("createWordsInput").value;
	var request = new XMLHttpRequest();
	request.onreadystatechange= function() {
	    if (request.readyState==4 && request.status==200) {
	    	console.log("hello");
	    	output.style.display = "block";
    		output.style.borderStyle = "solid";
    		output.style.borderColor = "green";
    		console.log(request.responseText);
    		var parsedStrings = unicodeArrayToStringArray(request.responseText);
    		var printOutput = printFormattedCalculated(parsedStrings);
    		var searchText = input;
    		document.getElementById("createWordsInput").value = "";
    		if (printOutput[1].substring(printOutput.length-2, printOutput.length) == "-0") {
    			output.style.textAlign = "center";
    			output.innerHTML = "No words from " + input[0] +", sorry.";
    			addSearch("Create: " + searchText + "&emsp; HighScore: No answers...");

    		}
    		else {
    			console.log(printOutput[1].substring(printOutput.length-1, printOutput.length));
	    		output.innerHTML = printOutput[0];
	    		addSearch("Create: " + searchText + "&emsp; HighScore: " + printOutput[1]);
	    	}
	    }
	}
 	input = input.split(" ");
 	console.log(input[0])
 	if (input[0].length > 8) {
 		console.log("If statement caught it.");
 		output.style.textAlign = "center";
 		output.innerHTML = "Please use 8 or less letters.<br />Any more takes too long to calculate.";
 		output.style.display = "block";
		output.style.borderStyle = "solid";
		output.style.borderColor = "green";
 		document.getElementById("createWordsInput").value = "";
 		return;
 	}
 	if (input.length == 1) {
 		//output.style.textAlign = "center";
	 	//console.log(input[0]);
	 	input[0] = input[0].toLowerCase();
	 	request.open("GET", "?request=generate&letters="+input[0]+"&boardWord=", "true");
	 	//console.log("Sent: calculateword.php?request=lookup&word="+input[0]);
	 	request.send();
	}
	else {
		input[0] = input[0].toLowerCase();
		request.open("GET", "?request=generate&letters="+input[0]+"&boardWord="+input[1], "true");
		request.send();
	}
}
function checkWords() {
	hideOutputs();
	var output = document.getElementById("checkWordsOutput");
	//output.style.display = "none"
	var input = document.getElementById("checkWordsInput").value;
	var request = new XMLHttpRequest();
	request.onreadystatechange=function() {
	    if (request.readyState==4 && request.status==200) {
	    	document.getElementById("checkWordsInput").value = "";
	    	console.log(request.responseText);
	    	if (request.responseText == "True") {
	    		output.style.display = "block";
	    		output.style.borderStyle = "solid";
	    		output.style.borderColor = "green";
	    		output.innerText = input + " is a word!";
	    		addSearch("Check: " + input + " &#x2713;");
	      		
	    	}
	    	else {
	    		output.style.display = "block";
	    		output.style.borderStyle = "solid";
	    		output.style.borderColor = "red";
	    		output.innerText = input + " is not word...";
	    		addSearch("Check: " + input + " &#x2715;");
	      		
	    	}
	    	
	    }
 	}
 	input = input.split(" ");
 	if (input.length == 1) {
 		output.style.textAlign = "center";
	 	console.log(input[0]);
	 	input[0] = input[0].toLowerCase();
	 	request.open("GET", "?request=lookup&word="+input[0], "true");
	 	console.log("Sent: ?request=lookup&word="+input[0]);
	 	request.send();
	 }
}

// document.getElementById("createForm").submit(function (event) {
// 	event.preventDefault();
// 	createWords();
// });