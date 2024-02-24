"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $gameScore = $('.game-score');
const $wordScore = $('.word-score');
const $time = $('#time');
const START_TIME = 60;

let gameId;
let time = 60;
let timerInterval;
$('.word-input-btn').on('click', handleWordSubmission);


/** Sends fetch request to API to start game and displays board. */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
  intervalId = setInterval(displayTime, 1000);
}

/** Creates game board and displays in DOM. */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  let $tbody = $('<tbody>');
  for (let row of board) {
    let $tr = $('<tr>');
    for (let cell of row) {
      let $td = $('<td>');
      $td.html(cell);
      $tr.append($td);
    }
    $tbody.append($tr);
  }
  $table.append($tbody);
}

/** Gets word from form, checks word validity, and displays result to DOM. */
async function handleWordSubmission(evt) {
  evt.preventDefault();
  const word = $wordInput.val();
  const result = await sendWordToAPI(word);
  displayWordResult(result, word);
  displayScores(result);

}

/** Takes string.Sends fetch request to API to check word validity and
 * returns result. */
async function sendWordToAPI(word) {
  const response = await fetch('/api/score-word', {
    method: "POST",
    body: JSON.stringify({ gameId: gameId, word: word }),
    headers: {
      "content-type": "application/json",
    }
  });
  return await response.json();
}

/** Takes API validity check result and word and either appends to played words
 * list or shows error message.
 */
function displayWordResult(result, word) {
  console.log("display word results");
  console.log(result);
  if (result.result == "ok") {
    $playedWords.append($('<li>').text(word));
  } else if (result.result == "not-on-board") {
    $message.html("Word is not on board!");
  } else if (result.result == "not-word") {
    $message.html("Word is not a word!");
  } else if (result.result == "duplicate-word") {
    $message.html("Word is duplicate!");
  }
}

function displayScores(result) {
  $wordScore.html(result.word_score);
  $gameScore.html(result.game_score);

}

function displayTime() {
  $time.html(`${--time} seconds`);
  if (time == 0) {
    clearInterval(timerInterval);
    $table.empty();
  }
}

start();