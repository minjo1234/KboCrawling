SELECT kboPitcher.playerId, kboPitcher.player_Name
FROM kboPitcher
         INNER JOIN kboPlayers
                    ON kboPitcher.playerId = kboPlayers.playerId
where kboPitcher.player_Name = kboPlayers.player_Name;
kboPlayers