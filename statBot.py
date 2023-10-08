from discord.ext import commands
from discord import Intents
import discord
import datetime
import pandas as pd
import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import nfl_data_py as nfl
import os
import urllib.request
import matplotlib.pyplot as pit
from matplotlib.offsetbox import AnnotationBbox
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

#async def statbot(ctx, playerName, weekNum, stat, year=datetime.datetime.now().year):

def snakeToTitle(snake_case):
    words = snake_case.split('_')
    titleWords = [word.capitalize() for word in words]
    return ' '.join(titleWords)

@bot.command()
async def statbot(ctx, *args):
    # weekNum must be in form of num
    # year is optional, default is current year
    if len(args) >= 2:
        playerName = ' '.join(args[:2])
    
    if len(args) < 4:
        await ctx.send("Invalid command format. $statbot <player name> <week> <stat> <year(optional>)")
        

    weekNum = args[2]
    stat = args[3]
    if len(args) < 5:
        year=datetime.datetime.now().year
    else:
        year = args[4]

    cleanWeek = int(weekNum)
    cleanYear = int(year)
    cleanName = playerName.title()
    weekly = nfl.import_weekly_data([int(cleanYear)])
    df = pd.DataFrame(weekly)
    playerData = df[df['player_display_name'] == cleanName]
    playerWeekData = playerData[playerData['week'] == cleanWeek]

    ### Parse all relevant stats for all positions weekly recap ####
    playerPosition = playerWeekData['position'].to_string(index=False)
    playerTeam = playerWeekData['recent_team'].to_string(index=False)
    playerSeason = playerWeekData['season'].to_string(index=False)
    playerOpponent = playerWeekData['opponent_team'].to_string(index=False)
    playerCompletions = playerWeekData['completions'].to_string(index=False)
    playerAttempts = playerWeekData['attempts'].to_string(index=False)
    playerPassingYards = playerWeekData['passing_yards'].to_string(index=False)
    playerPassingTds = playerWeekData['passing_tds'].to_string(index=False)
    playerInterceptionsThrown = playerWeekData['interceptions'].to_string(index=False)
    playerSacksTaken = playerWeekData['sacks'].to_string(index=False)
    playerSackYardsTaken = playerWeekData['sack_yards'].to_string(index=False)
    playerSackFumbles = playerWeekData['sack_fumbles'].to_string(index=False)
    playerSackFumblesLost = playerWeekData['sack_fumbles_lost'].to_string(index=False)
    playerPassing2ptConversions = playerWeekData['passing_2pt_conversions'].to_string(index=False)
    playerCarries = playerWeekData['carries'].to_string(index=False)
    playerRushingYards = playerWeekData['rushing_yards'].to_string(index=False)
    playerRushingTds = playerWeekData['rushing_tds'].to_string(index=False)
    playerRushingFumbles = playerWeekData['rushing_fumbles'].to_string(index=False)
    playerRushingFumblesLost = playerWeekData['rushing_fumbles_lost'].to_string(index=False)
    playerRushing2ptConversions = playerWeekData['rushing_2pt_conversions'].to_string(index=False)
    playerReceptions = playerWeekData['receptions'].to_string(index=False)
    playerTargets = playerWeekData['targets'].to_string(index=False)
    playerReceivingYards = playerWeekData['receiving_yards'].to_string(index=False)
    playerReceivingTds = playerWeekData['receiving_tds'].to_string(index=False)
    playerReceivingFumbles = playerWeekData['receiving_fumbles'].to_string(index=False)
    playerReceivingFumblesLost = playerWeekData['receiving_fumbles_lost'].to_string(index=False)
    playerYardsAfterCatch = playerWeekData['receiving_yards_after_catch'].to_string(index=False)
    playerReceiving2ptConversions = playerWeekData['receiving_2pt_conversions'].to_string(index=False)
    playerTargetShare = playerWeekData['target_share'].to_string(index=False)
    playerSpecialTeamsTds = playerWeekData['special_teams_tds'].to_string(index=False)
    playerFantasyPPR = playerWeekData['fantasy_points_ppr'].to_string(index=False)
    ###########################################################################

    playerTotalFumbles = playerWeekData['sack_fumbles'] + playerWeekData['rushing_fumbles'] + playerWeekData['receiving_fumbles']
    playerTotalFumblesStr = playerTotalFumbles.to_string(index=False)
    playerFumblesLost = playerWeekData['sack_fumbles_lost'] + playerWeekData['rushing_fumbles_lost'] + playerWeekData['receiving_fumbles_lost']
    playerFumblesLostStr = playerFumblesLost.to_string(index=False)

    cleanTargetShare = playerWeekData['target_share'] * 100
    cleanShare = cleanTargetShare.to_string(index=False)

    if (playerWeekData.empty):
        await ctx.send(f"It appears that this player was inactive for week #{cleanWeek}")
        


    if (stat == 'recap'):
        
        if (playerPosition == 'QB'):
            embed = discord.Embed(
            title = cleanName + ' Week ' + str(cleanWeek) + f' {playerSeason} ' + 'Recap',
            description = f'{playerTeam} {playerPosition}\n\nOpponent: {playerOpponent}\n\nPassing: \n{playerCompletions} / {playerAttempts} \nYards: {playerPassingYards} \nTouchdowns: {playerPassingTds} \n2pt Conversions: {playerPassing2ptConversions} \nSacks: {playerSacksTaken} \nSack Yards: {playerSackYardsTaken}\n\nRushing: \nCarries: {playerCarries} \nYards: {playerRushingYards} \nTouchdowns: {playerRushingTds} \n2pt Conversions: {playerRushing2ptConversions} \n\nReceiving: \n{playerReceptions} / {playerTargets} \nYards: {playerReceivingYards} \nYards After Catch: {playerYardsAfterCatch} \nTouchdowns: {playerReceivingTds} \n2pt Conversions: {playerReceiving2ptConversions} \nTarget Share: {cleanShare}% \n\nTurnovers: \nInterceptions: {playerInterceptionsThrown} \nFumbles: {playerTotalFumblesStr} \nFumbles Lost: {playerFumblesLostStr} \n\nSpecial Teams Tds: {playerSpecialTeamsTds}',
            color = discord.Color.green()
        )
            await ctx.send(embed=embed)

        elif (playerPosition == 'RB'):
            embed = discord.Embed(
            title = cleanName + ' Week ' + str(cleanWeek) + f' {playerSeason} ' + 'Recap',
            description = f'{playerTeam} {playerPosition}\n\nOpponent: {playerOpponent}\n\nPassing: \n{playerCompletions} / {playerAttempts} \nYards: {playerPassingYards} \nTouchdowns: {playerPassingTds} \n2pt Conversions: {playerPassing2ptConversions} \nSacks: {playerSacksTaken} \nSack Yards: {playerSackYardsTaken}\n\nRushing: \nCarries: {playerCarries} \nYards: {playerRushingYards} \nTouchdowns: {playerRushingTds} \n2pt Conversions: {playerRushing2ptConversions} \n\nReceiving: \n{playerReceptions} / {playerTargets} \nYards: {playerReceivingYards} \nYards After Catch: {playerYardsAfterCatch} \nTouchdowns: {playerReceivingTds} \n2pt Conversions: {playerReceiving2ptConversions} \nTarget Share: {cleanShare}% \n\nTurnovers: \nInterceptions: {playerInterceptionsThrown} \nFumbles: {playerTotalFumblesStr} \nFumbles Lost: {playerFumblesLostStr} \n\nSpecial Teams Tds: {playerSpecialTeamsTds}',
            color = discord.Color.green()
        )
            await ctx.send(embed=embed)

        elif (playerPosition == 'WR'):
            embed = discord.Embed(
            title = cleanName + ' Week ' + str(cleanWeek) + f' {playerSeason} ' + 'Recap',
            description = f'{playerTeam} {playerPosition}\n\nOpponent: {playerOpponent}\n\nPassing: \n{playerCompletions} / {playerAttempts} \nYards: {playerPassingYards} \nTouchdowns: {playerPassingTds} \n2pt Conversions: {playerPassing2ptConversions} \nSacks: {playerSacksTaken} \nSack Yards: {playerSackYardsTaken}\n\nRushing: \nCarries: {playerCarries} \nYards: {playerRushingYards} \nTouchdowns: {playerRushingTds} \n2pt Conversions: {playerRushing2ptConversions} \n\nReceiving: \n{playerReceptions} / {playerTargets} \nYards: {playerReceivingYards} \nYards After Catch: {playerYardsAfterCatch} \nTouchdowns: {playerReceivingTds} \n2pt Conversions: {playerReceiving2ptConversions} \nTarget Share: {cleanShare}% \n\nTurnovers: \nInterceptions: {playerInterceptionsThrown} \nFumbles: {playerTotalFumblesStr} \nFumbles Lost: {playerFumblesLostStr} \n\nSpecial Teams Tds: {playerSpecialTeamsTds}',
            color = discord.Color.green()
        )
            await ctx.send(embed=embed)

        elif (playerPosition == 'TE'):
            embed = discord.Embed(
            title = cleanName + ' Week ' + str(cleanWeek) + f' {playerSeason} ' + 'Recap',
            description = f'{playerTeam} {playerPosition}\n\nOpponent: {playerOpponent}\n\nPassing: \n{playerCompletions} / {playerAttempts} \nYards: {playerPassingYards} \nTouchdowns: {playerPassingTds} \n2pt Conversions: {playerPassing2ptConversions} \nSacks: {playerSacksTaken} \nSack Yards: {playerSackYardsTaken}\n\nRushing: \nCarries: {playerCarries} \nYards: {playerRushingYards} \nTouchdowns: {playerRushingTds} \n2pt Conversions: {playerRushing2ptConversions} \n\nReceiving: \n{playerReceptions} / {playerTargets} \nYards: {playerReceivingYards} \nYards After Catch: {playerYardsAfterCatch} \nTouchdowns: {playerReceivingTds} \n2pt Conversions: {playerReceiving2ptConversions} \nTarget Share: {cleanShare}% \n\nTurnovers: \nInterceptions: {playerInterceptionsThrown} \nFumbles: {playerTotalFumblesStr} \nFumbles Lost: {playerFumblesLostStr} \n\nSpecial Teams Tds: {playerSpecialTeamsTds}',
            color = discord.Color.green()
        )
            await ctx.send(embed=embed)

    else:
        
        playerWeekStatData = playerWeekData[stat].to_string(index=False)
        playerImage = playerWeekData['headshot_url']
        cleanStat = snakeToTitle(stat)
    
        embed = discord.Embed(
            title = cleanName + ' ' + cleanStat,
            description = playerWeekStatData,
            color = discord.Color.green()
        )
        await ctx.send(embed=embed)
    #embed.set_image(url=playerImage)

    # response = f"Player: {cleanName}\nWeek: {weekNum}\n{stat}: {playerWeekStatData}\nYear: {year}"
    # await ctx.send(response)

@bot.command()
async def statbothelp(ctx):

    weekly = nfl.import_weekly_data([2023])
    df = pd.DataFrame(weekly)
    weeklyColumns = df.columns
    greetingMessage1 = "Hello, I am StatBot. I can give you weekly stat recaps for NFL players! To use my services, simply enter the player's name, the week number of the season, and which stat you are looking for. You may enter recap to get all stats. You may also enter a year if you'd like stats from a previous season. "
    greetingMessage2 = "For example, enter the command !statbot Patrick Mahomes 3 recap 2022 and I will give you Patrick Mahomes stats from week 3 of 2022. You can leave the year off if you want stats from the current year!"
    helpMessage= "Enter the command $statbothelp at any time to repeat these instructions."
    statMessage = "Enter $statlist for a list of all available stats."
    #exampleMessage = "Enter $statbotexamples for further examples of commands you can use!"

    result = ''
    for weeklyCol in weeklyColumns:
        result += str(weeklyCol) + "\n"
    #print(result)
    response = f"{greetingMessage1}\n{greetingMessage2}\n{statMessage}\n{result}\n{helpMessage}"
    print(response)
    await ctx.send(response)

@bot.command()
async def statlist(ctx):
    weekly = nfl.import_weekly_data([2023])
    df = pd.DataFrame(weekly)
    weeklyColumns = df.columns

    greetingMessage1 ="You can search for individual player stats with the format - $statbot <player name> <week> <stat> <year(optional>)\n For example, $statbot Justin Fields 5 passing_tds would give you Justin Fields passing touchdowns from week 5 of 2023.  "
    statMessage = "I will list the different stats that I can find for you below - please enter them into your command exactly as I list them!"

    result = ''
    for weeklyCol in weeklyColumns:
        result += str(weeklyCol) + "\n"
    #print(result)
    response = f"{greetingMessage1}\n{greetingMessage2}\n{statMessage}\n{result}\n{helpMessage}"
    print(response)
    await ctx.send(response)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(status=discord.Status.online, activity = discord.Game("Type $help"))
    #await bot.process_commands()


bot.run('MTE1OTc4NDgzNDQ1ODIwNjI3OA.GnizVQ.B787SyznttWuDLuspPnSoaXs2qX9-OzRKewLvM')



    