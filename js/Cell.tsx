import cx from "classnames";
import React from "react";

export enum CellState {
  HIDDEN = 0,
  REVEALED = 1,
  FLAGGED = 2,
}

export interface Cell {
  state: CellState;
  count: number;
  mine: boolean;
}

export function Cell({
  row,
  col,
  cell,
}: {
  row: number;
  col: number;
  cell: Cell;
}) {
  return (
    <td
      data-row={row}
      data-col={col}
      className={cx(
        "border-gray-100 border w-8 h-8 text-center font-semibold minesweeper-cell",
        cell.state == CellState.REVEALED
          ? "bg-white cursor-default"
          : "bg-gray-300 border-gray-400 hover:bg-gray-200 cursor-pointer transition-colors",
        cell.state == CellState.REVEALED &&
          cell.count > 0 &&
          {
            1: "text-blue-600",
            2: "text-green-600",
            3: "text-red-600",
            4: "text-purple-600",
            5: "text-yellow-600",
            6: "text-pink-600",
            7: "text-black",
            8: "text-gray-800",
          }[cell.count]
      )}
    >
      {cell.state == CellState.HIDDEN
        ? ""
        : cell.state == CellState.FLAGGED
        ? "🚩"
        : cell.mine
        ? "💣"
        : cell.count == 0
        ? ""
        : cell.count}
    </td>
  );
}
