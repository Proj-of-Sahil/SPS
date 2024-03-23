from flask import Blueprint, render_template, jsonify, request
from flask_socketio import send, emit
from core import socketio
import json

home = Blueprint("home", __name__)


@home.route("/")
def home_html():
    return render_template("home.html")


lobbies = {}


@socketio.on("join_lobby")
def join_lobby(data):
    data = json.loads(data)
    lobby_id = data["lobby_id"]
    player_id = request.sid

    if lobby_id not in lobbies:
        lobbies[lobby_id] = []

    if len(lobbies[lobby_id]) < 2:
        if player_id in lobbies[lobby_id]:
            emit(
                "join_status",
                {"success": False, "message": "You are already in this lobby."},
                room=player_id,
            )
            return
        lobbies[lobby_id].append(player_id)
        emit(
            "join_status",
            {"success": True, "message": "Joined lobby successfully."},
            room=player_id,
        )
        if len(lobbies[lobby_id]) == 2:
            emit("game_start", {"message": "Game is starting."}, room=lobby_id)
    else:
        emit(
            "join_status",
            {"success": False, "message": "Lobby is full."},
            room=player_id,
        )


@socketio.on("leave_lobby")
def leave_lobby(data):
    data = json.loads(data)
    lobby_id = data["lobby_id"]
    player_id = request.sid

    if lobby_id not in lobbies:
        emit(
            "leave_status",
            {"success": True, "message": "Lobby does not exist."},
            room=player_id,
        )
        return

    if player_id not in lobbies[lobby_id]:
        emit(
            "leave_status",
            {"success": True, "message": "You are not in this lobby."},
            room=player_id,
        )
        return

    lobbies[lobby_id].remove(player_id)
    emit(
        "leave_status",
        {"success": True, "message": "Left lobby successfully."},
        room=player_id,
    )


@socketio.on("game")
def game(data):
    data = json.loads(data)
    player_id = request.sid
    lobby_id = data["lobbyID"]

    emit(
        "game_winner",
        {"winner": "player1"},
        room=player_id,
    )
