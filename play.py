#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea
from prompt_toolkit.completion import WordCompleter

import chess
import chess.engine

def main(play_with_engine=False):
    search_field = SearchToolbar()
    engine = None
    if play_with_engine:
      engine = chess.engine.SimpleEngine.popen_uci('/usr/bin/stockfish')
    board = chess.Board()
    chess_completer = WordCompleter([str(x) for x in board.legal_moves])

    output_field = TextArea(style="class:output-field", text=board.unicode())
    input_field = TextArea(
        height=1,
        prompt=">>> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
        search_field=search_field,
        completer = chess_completer,
        complete_while_typing=True
    )
    container = HSplit(
        [
            output_field,
            Window(height=1, char="-", style="class:line"),
            input_field,
            search_field,
        ]
    )

    def accept(buff):
        new_move = chess.Move.from_uci(input_field.text)
        board.push(new_move)

        if engine:
          result = engine.play(board, chess.engine.Limit(time=0.1))
          board.push(result.move)

        output = board.unicode()
        output_field.buffer.document = Document(
            text = output
        )

        input_field.completer = WordCompleter([str(x) for x in board.legal_moves])

    input_field.accept_handler = accept

    kb = KeyBindings()

    @kb.add("c-c")
    def app_exit(event):
        event.app.exit()

    style = Style(
        [
            ("output-field", "bg:#000044 #ffffff"),
            ("input-field", "bg:#000000 #ffffff"),
            ("line", "#004400"),
        ]
    )

    application = Application(
        layout=Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=True,
    )

    application.run()

if __name__ == "__main__":
    main(play_with_engine=True)
