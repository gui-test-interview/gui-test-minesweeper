import axios from "axios";
import React from "react";
import ReactDOM from "react-dom";
import cx from "classnames";
import {
  BrowserRouter,
  Switch,
  Route,
  Link,
  useHistory,
} from "react-router-dom";
import { DateTime } from "luxon";
import Game, { Game as GameType, GameState } from "./Game";

import "./styles.css";

function GameList() {
  const [, setTick] = React.useState({});
  const [games, setGames] = React.useState<GameType[]>(null);

  // On render, query the endpoint to get the list of games.
  React.useEffect(() => {
    axios.get("/").then((result) => setGames(result.data));
  }, []);

  // Re-render every second to update timestamps.
  React.useEffect(() => {
    const interval = setInterval(() => {
      setTick({});
    }, 1000);
    return () => clearInterval(interval);
  });

  return (
    <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {games &&
        games.map((game) => (
          <Link
            to={game.url}
            key={game.id}
            className={cx(
              "rounded p-4 my-2 bg-gray-50 border border-gray-200 flex flex-col",
              game.state == GameState.STARTED &&
                "text-green-600 border-green-600"
            )}
          >
            <span>
              <span className="mr-2">
                {game.state == GameState.STARTED
                  ? DateTime.local()
                      .diff(DateTime.fromISO(game.dateStarted), [
                        "minutes",
                        "seconds",
                      ])
                      .toFormat("mm:ss")
                  : DateTime.fromISO(game.dateEnded).toLocaleString(
                      DateTime.DATETIME_SHORT
                    )}
              </span>
              {game.state == GameState.WON ? (
                <span className="rounded text-xs px-2 py-0.5 bg-green-600 text-white font-bold">
                  WON
                </span>
              ) : game.state == GameState.LOST ? (
                <span className="rounded text-xs px-2 py-0.5 bg-red-600 text-white font-bold">
                  LOST
                </span>
              ) : (
                <span>{Math.round(game.progress * 100)}% complete</span>
              )}
            </span>
            <span className="text-gray-500 text-sm">
              {game.width} x {game.height}, {game.mines} mines
            </span>
          </Link>
        ))}
    </section>
  );
}

interface GameSettings {
  width: number;
  height: number;
  mines: number;
}

function NewGameButton({
  settings,
  ...props
}: { settings: GameSettings } & React.ComponentPropsWithRef<"button">) {
  const history = useHistory();

  function onNewGameClicked() {
    axios
      .post("/", settings)
      .then((result) => result.data as GameType)
      .then((game) => history.push(game.url));
  }

  return (
    <button
      className="inline-flex items-center px-2 py-1 ml-1 border border-transparent \
rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 \
focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      onClick={onNewGameClicked}
      {...props}
    >
      {props.children}
    </button>
  );
}

/**
 * Root component. Renders a fixed header with a button for a new game, along with
 * either a list of games or the currently-selected game based on the URL path.
 */
function App(): React.ReactElement {
  return (
    <BrowserRouter>
      <header className="flex flex-row mb-4">
        <h1 className="flex-grow flex-shrink text-3xl font-semibold">
          <Link to="/">Minesleeper</Link>
        </h1>
        <div className="">
          New game:
          <NewGameButton settings={{ width: 9, height: 9, mines: 10 }}>
            Easy
          </NewGameButton>
          <NewGameButton settings={{ width: 16, height: 16, mines: 40 }}>
            Intermediate
          </NewGameButton>
          <NewGameButton settings={{ width: 30, height: 16, mines: 99 }}>
            Expert
          </NewGameButton>
        </div>
      </header>
      <Switch>
        <Route path="/:id">
          <Game />
        </Route>
        <Route path="/">
          <GameList />
        </Route>
      </Switch>
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.getElementById("main"));

if (module.hot) {
  module.hot.accept();
}
