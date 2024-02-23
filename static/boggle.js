"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;
$('.word-input-btn').on('click', newWordApi);


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

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


async function newWordApi(evt) {
  evt.preventDefault();
  const response = await fetch('/api/score-word', {
    method: "POST",
    body: JSON.stringify({ gameId: gameId, word: $wordInput.val() }),
    headers: {
      "content-type": "application/json",
    }
  });

  const result = await response.json();
  console.log(result);

}

start();