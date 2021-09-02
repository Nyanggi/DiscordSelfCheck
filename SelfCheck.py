import discord
import datetime
import hcskr
from discord.ext import commands

prefix = "본인의 접두사"
bot = commands.Bot(command_prefix = prefix)
error_embed_color = 0xff0008
success_embed_color = 0x00ff37

@bot.event
async def on_ready():
    print("{0.user}에 로그인하였습니다!".format(bot))
    

@bot.command(aliases=['진단등록', '진단토큰'])
async def 토큰생성(ctx, name=None, birth=None, area=None, level=None, schoolname=None, password=None):
    if name == None or birth == None or area == None or level == None or schoolname == None or password == None:
        embed = discord.Embed(title=":x: 올바른 값을 입력해 주세요", color=error_embed_color)
        embed.add_field(name="이렇게 입력할 수 있어요",
                        value="```" + prefix + "토큰생성 [이름] [생년월일 6자리] [지역] [학교급] [학교명] [자가진단 비밀번호]```", inline=True)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.channel.send(embed=embed)
    else:
        result = await hcskr.asyncGenerateToken(name, birth, area, schoolname, level, password)
        if result['error'] == True:
            embed = discord.Embed(title=":x: 오류가 발생했어요!", color=error_embed_color)
            embed.add_field(name="오류 내용", value=f"```{result['message']}```", inline=True)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            return await ctx.channel.send(embed=embed)
        else:
            if not ctx.guild:
                embed = discord.Embed(title=f"자가진단 토큰생성 완료!", description=result['token'], color=success_embed_color)
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=":x: DM에서 실행해 주세요", description='이 명령어는 DM에서만 사용할 수 있어요', color=error_embed_color)
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                return await ctx.channel.send(embed=embed)


@bot.command()
async def 진단하기(ctx, hcs_token=None):
    if hcs_token == None:
        embed = discord.Embed(title=":x: 자가진단 토큰을 입력해 주세요", color=error_embed_color)
        embed.add_field(name="이렇게 입력할 수 있어요", value="```" + prefix + "진단하기 [토큰]```", inline=True)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.channel.send(embed=embed)
    else:
        result = await hcskr.asyncTokenSelfCheck(hcs_token)
        print(result)
        if result['error'] == True:
            embed = discord.Embed(title=":x: 오류가 발생했어요!", color=error_embed_color)
            embed.add_field(name="오류 내용", value=f"```{result['message']}```", inline=True)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            return await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=f"자가진단 완료!", description=f"{result['regtime']}에 자가진단을 완료했어요",
                                  color=success_embed_color)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            
            
bot.run("봇 토큰")
