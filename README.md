# Minesleeper

This is a clone of the popular game of [Minesweeper]! If you have never played it
before, you can try playing the game by [searching for "minesweeper" in google].

The premise of the game is simple: a field is filled with hidden mines; the objective
is to locate them by revealing squares on the grid. Each square that does not contain a
mine has a number from 1-8 indicating the number of surrounding mines (or blank if 0).
If a mine is revealed, the game is lost. To help with reasoning, the player can flag
cells that they believe contain mines by right-clicking.

[minesweeper]: https://en.wikipedia.org/wiki/Minesweeper_(video_game)
[searching for "minesweeper" in google]: https://www.google.com/search?q=play+minesweeper

## The Task

The game is playable; however, there are a few missing features, bugs and usability issues.

1. "Cell expansion" is not implemented. When clicking a cell with no surrounding mines,
   all adjacent cells should be revealed as well (and if any of those have no
   surrounding mines, their neighbors should be revealed in turn, and so on).
2. There is no checking for win/loss states. If a mine is clicked, the game should be
   lost and all mines should be shown to the user along with an indication of which
   flags were incorrectly marked. If every non-mine cell is revealed, the game should be
   won. Any interaction with a finished game should also be disabled.
3. It is possible to lose on the first click by revealing a mine. Improve this
   experience so that the first cell clicked is never a mine.
4. Show a timer at the top of the game along with a count of the number of
   remaining mines (total mines minus the number of flags placed).
5. Implement double-clicking on a revealed cell to automatically expand
   neighbors. This is extremely useful when playing quickly, and in most implementations
   is performed by clicking both left/right mouse buttons at once. This works by
   checking if the number of flags around a cell matches its count; if so, all unflagged
   neighbors are revealed. If the count does not match, nothing happens. (If a flag was
   misplaced, this can cause the game to be lost.)

To submit your work, first check out a new branch. Implement each task as a separate commit
on that branch, push your changes and open a Pull Request into the `main` branch along with
a brief explanation. If you aren't able to finish every task in time, don't worry - just
submit whatever you are able to complete within the 3-hour timeframe.

## Setup

> NOTE: If you are using VSCode and have Docker installed, you can use the [Remote - Containers]
> VSCode extension to set up the project automatically.

[remote - containers]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

Prior to starting, you will need a working installation of [Python 3.9] and [Node 14].
How to do this depends on your operating system - please see each project's page for
more details. (Older versions of Python may work, but you may run into issues with
JSON support in SQLite; there are [instructions here](https://code.djangoproject.com/wiki/JSON1Extension)
on how to work around this.)

To run the game locally, clone this repository onto your local machine. From the
directory where the code is checked out, the first step is to initialize your Python
virtual environment - this is where Django and a few other dependencies will be
installed. The commands below will create a brand new virtual environment in a `.pyenv`
folder in the current directory, activate it (so that subsequent commands run within the
environment), and then install the dependencies listed in `requirements.txt`:

    python3 -m venv .pyenv
    source .pyenv/bin/activate
    pip install -r requirements.txt

Note: the second command to activate the environment also depends on your platform and
shell. The example above is for bash on POSIX; for other systems, please see the [venv
documentation].

You will also need to install the frontend dependencies specified in `package.json`. To
do this, run the following command from the same directory:

    npm install

This will create a `node_modules` folder containing the installed dependencies.

Finally, you will need to create the SQLite database that will contain game data. This
is done by [applying Django migrations]:

    ./manage.py migrate

If you make any changes to models, be aware that you will need to create a new migration
and apply it to your database.

[python 3.9]: https://www.python.org/downloads/
[node 14]: https://nodejs.org/en/download/
[venv documentation]: https://docs.python.org/3/library/venv.html#creating-virtual-environments
[applying django migrations]: https://docs.djangoproject.com/en/3.1/topics/migrations/

## Running

To start the app, you will need to run two separate commands in parallel (i.e. two
terminals). In one, start the Django server:

    ./manage.py runserver

In the other, start the Parcel bundler process:

    npm run dev

This will watch for changes to TypeScript and CSS files and automatically reload the
page. The game should now be accessible in your browser via http://localhost:8000.

You can also run the test suite by running:

    pytest

## Documentation

### Folder Structure

Here are the main folders and files within this repository:

- [`app`](./app): contains the Django project settings as well as top-level URLs. You
  shouldn't need to change these files.
- [`game`](./game): the primary server-side game code as a Django app.
  - [`game/models.py`](./game/models.py): contains the `Game` model and related logic.
  - [`game/serializers.py`](./game/serializers.py): uses Django REST Framework to expose
    a REST API for accessing game data.
- [`js`](./js): frontend React code and stylesheet.
  - [`js/index.tsx`](./js/index.tsx): React root and index page listing games.
  - [`js/Game.tsx`](./js/Game.tsx): the game board.
  - [`js/Cell.tsx`](./js/Cell.tsx): an individual cell on a board.

### Dependencies

Here is a list of the important technologies used in this project:

- [Django]: web framework
- [Django REST Framework]: toolkit for building RESTful web APIs in Django
- [TypeScript]: typed JavaScript
- [React]: frontend framework for building declarative user interfaces
- [Tailwind CSS]: utility-first CSS framework used for frontend styling

A few other dependencies that are used and may be useful:

- [React Router]: declarative navigation and router for React
- [Classnames]: a simple utility for combining classnames
- [Axios]: `Promise`-based HTTP client
- [Luxon]: friendly wrapper for Javascript dates and times

See each project's page for more in-depth documentation and reference.

[django]: https://docs.djangoproject.com/en/
[django rest framework]: https://www.django-rest-framework.org/
[typescript]: https://www.typescriptlang.org/
[react]: https://reactjs.org/
[tailwind css]: https://tailwindcss.com/docs
[react router]: https://reacttraining.com/react-router/
[classnames]: https://jedwatson.github.io/classnames/
[axios]: https://github.com/axios/axios
[luxon]: https://moment.github.io/luxon/
