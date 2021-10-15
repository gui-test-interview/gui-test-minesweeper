import axios from "axios";
import React from "react";
import { useLocation } from "react-router-dom";

import { CellState, Cell } from "./Cell";

export enum GameState {
  STARTED = 0,
  WON = 1,
  LOST = 2,
}

export interface Game {
  id: string;
  url: string;
  width: number;
  height: number;
  mines: number;
  progress: number;
  state: GameState;
  dateStarted: string;
  dateEnded: string;
  board: Cell[][];
}

export default function Game() {
  const location = useLocation();
  const [game, setGame] = React.useState<Game>(null);

  const cellClicked = React.useCallback<React.MouseEventHandler>(
    (e) => {
      const { row, col } = (e.target as HTMLElement).dataset;
      const [i, j] = [parseInt(row), parseInt(col)];

      e.preventDefault();

      if (e.button == 2 && game.board[i][j].state != CellState.REVEALED) {
        axios
          .post("reveal/", { row: i, col: j, flag: true })
          .then((result) => setGame(result.data));
      } else if (e.button == 0 && game.board[i][j].state == CellState.HIDDEN) {
        axios
          .post("reveal/", { row: i, col: j })
          .then((result) => setGame(result.data));
      }
    },
    [game]
  );

  const cellDoubleClicked = React.useCallback<React.MouseEventHandler>((e) => {
    const { row, col } = (e.target as HTMLElement).dataset;

    // TODO: double-click to auto-expand

    e.preventDefault();
  }, []);

  React.useEffect(() => {
    axios.get("").then((result) => setGame(result.data));
  }, [location]);

  return (
    <div className="overflow-x-auto">
      <table
        className="select-none mx-auto my-6"
        onClick={cellClicked}
        onDoubleClick={cellDoubleClicked}
        onContextMenu={cellClicked}
      >
        <tbody>
          {game &&
            game.board.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => (
                  <Cell key={j} row={i} col={j} cell={cell} />
                ))}
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}
