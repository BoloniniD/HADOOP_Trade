import sys
import moex_api

import telebot


class HaboobaBot:
    trades_: moex_api.Trades

    def __init__(self):
        self.trades_ = moex_api.Trades()
        cfg = open("token.txt", "r")
        try:
            token = cfg.readline()
            self.bot = telebot.TeleBot(token)
        except Exception as e:
            print(f"Cannot open configs. Reason: {e}")
            cfg.close()
            sys.exit()
        finally:
            cfg.close()

        @self.bot.message_handler(commands=["start"])
        def startBot(message):
            # reply to start command
            print("Received start message")
            self.bot.reply_to(
                message,
                "This bot will show you the what you strategy should look like from some point in the past.\n"
                "Type /help to see the list of commands"
            )

        @self.bot.message_handler(commands=["help"])
        def helpBot(message):
            # reply to help command
            print("Received help message")
            self.bot.reply_to(
                message,
                "/start - start bot\n"
                "/help - show this message\n"
                "/get_strategy <date(YYYY-MM-DD)> <MOEX code> <phase of day(OPEN/CLOSE)>(e.g. 2002.05.03 YNDX OPEN"
            )

        @self.bot.message_handler(commands=["get_strategy"])
        def getStrategyBot(message: telebot.types.Message):
            # reply to add_config command
            print("Received get_strategy message")

            date, code, phase = message.text.split()[1:]

            if phase not in {"mourning", "evening"}:
                self.bot.reply_to(
                    message,
                    "Please choose phase of day correctly: OPEN/CLOSE"
                )
                return

            self.trades_.user_request(date, code, phase)

            self.bot.reply_to(
                message,
                self.trades_.user_request(date, code, phase)
            )

    def launchBot(self):
        # start polling
        print("Launching bot...")
        self.bot.polling()


if __name__ == "__main__":
    tbot = HaboobaBot()
    tbot.launchBot()
