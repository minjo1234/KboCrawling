SELECT kboPitcher.playerId, kboPitcher.playerName
FROM kboPitcher
INNER JOIN kboPlayers
ON kboPitcher.playerId = kboPlayers.playerId;