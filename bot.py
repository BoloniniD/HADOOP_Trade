import sys
from datetime import datetime

import moex_api

import telebot

stocks = {'RASP', 'MAGN', 'HALS', 'ROSN', 'PIKK', 'VTBR', 'PHST', 'TRMK', 'LSRG', 'MVID', 'NMTP', 'AFKS', 'HYDR',
          'BSPB', 'MRKP', 'OGKB', 'pnpo', 'AFLT', 'AKRN', 'ARSA', 'arsb', 'ASSB', 'AVAZ', 'blsbp', 'CHMF', 'CHZN',
          'CLSB', 'CLSBP', 'DASB', 'DGBZ', 'DIXY', 'dvsbp', 'DVEC', 'GAZP', 'GMKN', 'IRGZ', 'IRKT', 'ISKJ', 'KBSB',
          'KCHE', 'KLSB', 'KMAZ', 'KROT', 'KRSG', 'KTSB', 'KTSBP', 'KUBE', 'KMEZ', 'KZMS', 'LKOH', 'LPSB', 'LSNG',
          'LSNGP', 'MGNT', 'MISB', 'MISBP', 'MMBM', 'MRSB', 'MSNG', 'MSRS', 'MSSB', 'MTSS', 'NLMK', 'NNSB', 'NNSBP',
          'NVTK', 'UPRO', 'ENRU', 'OMZZP', 'PLZL', 'PMSB', 'PMSBP', 'PRIM', 'ROSB', 'RTKM', 'RTKMP', 'RTSB', 'RTSBP',
          'fpbn', 'GUMM', 'KROTP', 'MFGS', 'MFGSP', 'APTK', 'bstp', 'MGTSP', 'MGTS', 'PRMB', 'TATN', 'TATNP', 'RZSB',
          'SBER', 'SBERP', 'SIBN', 'SNGS', 'SNGSP', 'STSB', 'STSBP', 'SVAV', 'BELU', 'TASB', 'TASBP', 'TGKA', 'TGKB',
          'TGKBP', 'TGKD', 'TGKDP', 'tgkj', 'TGKN', 'TORS', 'TORSP', 'tosb', 'TRNFP', 'TTLK', 'URKA', 'UTAR', 'VDSB',
          'VGSB', 'VGSBP', 'VLHZ', 'vosb', 'VRSB', 'VRSBP', 'VSMO', 'VTGK', 'WTCM', 'WTCMP', 'YKEN', 'YRSB', 'YRSBP',
          'YRSL', 'ZMZN', 'ZMZNP', 'GCHE', 'NKNC', 'NKNCP', 'RKKE', 'MRKV', 'MRKC', 'KZBE', 'MRKK', 'MRKZ', 'MRKS',
          'MRKU', 'FEES', 'MRKY', 'MTLRP', 'KCHEP', 'YKENP', 'INGR', 'UKUZ', 'FESH', 'KOGK', 'AMEZ', 'TUZA', 'RUSP',
          'ROST', 'CNTL', 'KUSTP', 'RODNP', 'ODVA', 'sntz', 'svtz', 'MGNZ', 'gsen', 'GAZA', 'JNOS', 'MOTZ', 'benr',
          'benrp', 'MTLR', 'KRSBP', 'KRSB', 'gznp', 'LNZL', 'CHKZ', 'CHMK', 'MERF', 'VRAO', 'RSTI', 'RSTIP', 'CHEP',
          'sumz', 'OSMP', 'BLNG', 'mgok', 'udmn', 'AVAZP', 'REBR', 'LNZLP', 'VRAOP', 'OMSH', 'AQUA', 'KBTK', 'PRTK',
          'BISV', 'BISVP', 'DIOD', 'SXPNP', 'JNOSP', 'TRCN', 'MSTT', 'MAGE', 'MAGEP', 'LIFE', 'RBCM', 'DZRD', 'DZRDP',
          'TUCH', 'YASH', 'TAER', 'msfb', 'kcik', 'tuma', 'tumap', 'PLSM', 'NFAZ', 'SELG', 'GAZC', 'GAZS', 'SAGO',
          'SAGOP', 'CNTLP', 'ZVEZ', 'BANE', 'BANEP', 'SARE', 'SAREP', 'RUSI', 'ALRS', 'RUGR', 'ALNU', 'BRZL', 'CHGZ',
          'ELTZ', 'HIMC', 'HIMCP', 'IGST', 'IGSTP', 'KAZT', 'KAZTP', 'KMTZ', 'KRKN', 'KRKNP', 'KRKO', 'KRKOP', 'KUNF',
          'KZOS', 'MORI', 'MUGS', 'MUGSP', 'NAUK', 'NKSH', 'PAZA', 'TANL', 'TANLP', 'TGKO', 'ufosp', 'USBN', 'VJGZ',
          'VJGZP', 'YAKG', 'zemc', 'ZILL', 'ziop', 'MGVM', 'NPOF', 'KZOSP', 'NSVZ', 'GAZT', 'FORTP', 'PHOR', 'igip',
          'PRFN', 'UNKL', 'SELGP', 'URKZ', 'ALBK', 'MOBB', 'KUZB', 'KGKC', 'MFON', 'VSYDP', 'VSYD', 'ABRD', 'KGKCP',
          'RTGZ', 'LVHK', 'RLMN', 'MSST', 'rtbgp', 'MOEX', 'GTLC', 'UCSS', 'DALM', 'irpa', 'irpap', 'mefr', 'mush',
          'mzik', 'mzikp', 'rtvl', 'POLY', 'ZHIV', 'ROLO', 'UNAC', 'RDRB', 'RGSS', 'mtpv', 'CBOM', 'DSKY', 'RLMNP',
          'YNDX', 'aakp', 'acru', 'afmc', 'akil', 'aklc', 'aklcp', 'alnpp', 'amnep', 'angg', 'arse', 'asco', 'asog',
          'astm', 'atlm', 'aves', 'avgt', 'avio', 'bchv', 'belzp', 'bisi', 'bkog', 'blrep', 'bmkk', 'bmko', 'bmsm',
          'bogz', 'borg', 'brog', 'brsz', 'brszp', 'brtk', 'btsm', 'btst', 'bunzp', 'bzav', 'cegz', 'cegzp', 'cems',
          'cenh', 'cenhp', 'chge', 'chrm', 'cinb', 'city', 'comz', 'cryd', 'dbkm', 'dnpp', 'duks', 'elag', 'elar',
          'elgz', 'elgzp', 'elst', 'engr', 'ensk', 'fenz', 'fztr', 'gdsop', 'gpvn', 'gsgz', 'gsov', 'gsrb', 'gtng',
          'gtngp', 'guke', 'gukep', 'gyaa', 'gzas', 'gzavp', 'gzes', 'hanf', 'hanfp', 'hkez', 'hmds', 'hmtz', 'hnpz',
          'hnpzp', 'iaph', 'ilim', 'irog', 'iskc', 'iskrp', 'iznm', 'iznmp', 'kadv', 'kbaa', 'kbaap', 'kemz', 'keskp',
          'kfar', 'kgaz', 'kgazp', 'kgesp', 'khlb', 'khlt', 'kimp', 'klgz', 'klmz', 'klog', 'kmap', 'kmzap', 'kmzm',
          'knms', 'komz', 'krgm', 'krgs', 'krnf', 'krnfp', 'krvapc', 'ktrsp', 'ktyr', 'ktyrp', 'kunp', 'kuog', 'kuvz',
          'kvet', 'kymz', 'kymzp', 'kzhb', 'kzizp', 'kzmk', 'kzom', 'leog', 'lepsp', 'lldk', 'lpog', 'lsmz', 'metp',
          'metz', 'metzp', 'mksh', 'mlnk', 'mmmz', 'mmtp', 'moib', 'mscp', 'msib', 'msts', 'mstz', 'mtpvp', 'mtst',
          'murt', 'mvzmp', 'mynt', 'myntp', 'mzdr', 'ncos', 'nefz', 'nefzp', 'nfmt', 'nkes', 'nkshp', 'nnog', 'nompp',
          'norr', 'nppa', 'npps', 'nppsp', 'nrgp', 'nsrz', 'nsrzp', 'ntcz', 'nzhs', 'obne', 'obrpp', 'oeng', 'okby',
          'okbyp', 'okes', 'onps', 'ords', 'orfe', 'orfep', 'pbdt', 'pdmb', 'penm', 'pgmt', 'pgzf', 'plzi', 'pmoz',
          'pren', 'prnp', 'prnpp', 'prsn', 'ratp', 'rdne', 'ritm', 'rncu', 'rncup', 'rotp', 'rpkb', 'rpsz', 'rtim',
          'rtlm', 'ryazp', 'rzcm', 'rzog', 'sagz', 'sbenp', 'sbgz', 'semp', 'sevg', 'skai', 'slme', 'slst', 'smnf',
          'smnfp', 'smpp', 'spkm', 'spkmp', 'stkgp', 'svfr', 'szuc', 'szucp', 'szve', 'szvs', 'tafn', 'tatf', 'tlaz',
          'tlnpp', 'tmeu', 'tmgz', 'tmpa', 'tmpap', 'tmpsb', 'tmpsp', 'tobm', 'togz', 'toms', 'tpop', 'trgmp', 'trmz',
          'tsgi', 'ttos', 'tuaz', 'tuog', 'tvag', 'tveo', 'txsv', 'tymt', 'tymtp', 'typmp', 'tzkm', 'uelm', 'ugnf',
          'ukgs', 'uppo', 'upszp', 'ural', 'uramp', 'urap', 'urapp', 'urhc', 'utbn', 'uzrt', 'vakz', 'varn', 'varnp',
          'vazz', 'vbbn', 'vbbnp', 'vbmg', 'vdok', 'vflt', 'vgap', 'vlgm', 'vlog', 'vngf', 'vngfp', 'vnipp', 'vnzm',
          'vomd', 'vorgp', 'vsrp', 'vugk', 'yarzp', 'ymnpp', 'zemcp', 'zent', 'zhdy', 'zillp', 'zkom', 'zsgpp', 'zzgt',
          'acbk', 'acnd', 'aetz', 'aetzp', 'agrt', 'akam', 'akbr', 'akcm', 'akgs', 'akib', 'akmz', 'aktt', 'alfs',
          'almzp', 'alnp', 'amne', 'anap', 'anapp', 'ange', 'angs', 'apkm', 'apmo', 'apsz', 'armg', 'armk', 'armz',
          'armzp', 'arpc', 'arpo', 'arpop', 'arzo', 'asko', 'atea', 'atep', 'atlmp', 'attr', 'avdz', 'avdzp', 'avnt',
          'avsi', 'avsk', 'avsu', 'azri', 'basc', 'belc', 'belz', 'bemz', 'beto', 'bgdv', 'bges', 'bgesp', 'bioh',
          'bios', 'biosp', 'biru', 'blhk', 'blhkp', 'blmz', 'blph', 'blre', 'bmkkp', 'bmkop', 'bmsmp', 'bngf', 'bogn',
          'brad', 'brar', 'brarp', 'brzlp', 'bstd', 'bstdp', 'btsmp', 'btstp', 'bunz', 'buth', 'buthp', 'bvml', 'bzavp',
          'ccbk', 'ccsg', 'cdst', 'cdstp', 'chcb', 'chkzp', 'chlb', 'chog', 'chsk', 'chvp', 'chzb', 'cmlz', 'dadz',
          'dadzp', 'dcnu', 'dkko', 'dlgs', 'donm', 'dorf', 'dors', 'dskt', 'elcm', 'elkd', 'elvp', 'elvpp', 'embn',
          'ensb', 'espm', 'fast', 'ffsp', 'fpmg', 'frmc', 'frmcp', 'galo', 'gbkl', 'gbst', 'gdso', 'ggok', 'gips',
          'gipsp', 'gmst', 'gnyap', 'gpvnp', 'gsgzp', 'gybb', 'gybbp', 'gykp', 'gzav', 'gzpr', 'gztm', 'hlfs', 'hlnb',
          'hmdsp', 'hmtzp', 'iaphp', 'iesk', 'inec', 'GTSS', 'ings', 'inst', 'iskr', 'iskz', 'itrg', 'ivog', 'ivogp',
          'izhz', 'izhzp', 'izub', 'izubp', 'kabe', 'kabep', 'kadvp', 'karb', 'kasu', 'kbkc', 'kbvp', 'kchu', 'kchup',
          'kems', 'kemzp', 'kesk', 'ketz', 'kgas', 'kges', 'kggk', 'khelp', 'khgf', 'kksm', 'klmzp', 'kmae', 'kmaep',
          'kmpv', 'kmtx', 'kmza', 'kngz', 'konf', 'kons', 'koog', 'kosm', 'kpmg', 'kpmo', 'krfm', 'krgg', 'krgmp',
          'krgz', 'krog', 'krop', 'krpe', 'krts', 'krva', 'krvapa', 'krvapb', 'ksin', 'ksinp', 'ksiz', 'ksmv', 'ksmvp',
          'ktrs', 'kuav', 'kubm', 'kuch', 'kunpp', 'kuvp', 'kvetp', 'kzae', 'kzaep', 'kzbg', 'kzff', 'kzhk', 'kziz',
          'kzkm', 'kzkmp', 'kzru', 'kzsb', 'kzts', 'kzvs', 'lamz', 'lamzp', 'lato', 'legs', 'leps', 'lhmp', 'liks',
          'likz', 'ljaz', 'lorp', 'lorpp', 'lots', 'maku', 'maln', 'maru', 'mayk', 'maykp', 'mbrd', 'mbsppc', 'mdcm',
          'meat', 'mecf', 'mecfp', 'memy', 'metn', 'metpp', 'mhkn', 'mkpz', 'mkro', 'mler', 'mlzg', 'mmtpp', 'mmzv',
          'mosc', 'mpch', 'mpdz', 'mpor', 'mporp', 'mpsm', 'mpsmp', 'msbo', 'mscpp', 'mshl', 'mshr', 'mshz', 'msin',
          'msir', 'msot', 'mstf', 'mstzp', 'mtpl', 'mtrx', 'mtstp', 'mvzm', 'mzbk', 'mzsm', 'mzsmp', 'nbam', 'nbamp',
          'ngok', 'ngor', 'ngrm', 'nhfm', 'nipgp', 'noer', 'nole', 'npcs', 'nrbm', 'nrgy', 'nsng', 'ntzl', 'nzdsp',
          'nzhkp', 'obnep', 'obrp', 'oelm', 'ogex', 'oken', 'okesp', 'oksa', 'omka', 'omog', 'omogp', 'omrp', 'omrpp',
          'omsv', 'opro', 'orgn', 'orgz', 'orls', 'orog', 'osrp', 'ozga', 'pbgzp', 'pbtf', 'pdnz', 'pehl', 'pekr',
          'pekrp', 'penmp', 'pgho', 'pirop', 'pkez', 'plzip', 'pmzv', 'pnaz', 'pnhm', 'pnhmp', 'poek', 'poup', 'pprt',
          'pprtp', 'prbn', 'prenp', 'prep', 'prgr', 'prib', 'pribp', 'priz', 'prkb', 'prmg', 'prmz', 'prsk', 'psol',
          'ptpa', 'ptpap', 'pzkm', 'pzkmp', 'rarz', 'rdnep', 'rfmc', 'rfrt', 'rkch', 'rkchp', 'rkrz', 'rtlmp', 'rtpt',
          'rubt', 'ruhm', 'rzmk', 'salz', 'sarn', 'sarnp', 'sbah', 'sben', 'sbgs', 'sckk', 'sdmb', 'sdmbp', 'segz',
          'sepo', 'sfmd', 'sgat', 'sgatp', 'sgaz', 'shaz', 'shazp', 'shls', 'shvz', 'sibc', 'sina', 'sinap', 'skbp',
          'skcm', 'skgd', 'skpr', 'skzk', 'SLEN', 'slmep', 'slnt', 'smgf', 'smgfp', 'smlz', 'smog', 'smyk', 'snfg',
          'snfgp', 'sngf', 'sngfp', 'sogp', 'sogs', 'soli', 'sovp', 'spib', 'spkep', 'spkrp', 'splk', 'sprv', 'spsb',
          'srog', 'stgz', 'stgzp', 'stkg', 'strm', 'strn', 'strnp', 'svmt', 'svna', 'svnap', 'svtg', 'sysy', 'szrt',
          'sztt', 'tafnp', 'takb', 'tavrp', 'taxf', 'taxn', 'tens', 'teod', 'terl', 'tgmp', 'tgmpp', 'thpr', 'thprp',
          'tish', 'tlnp', 'tlvs', 'tmas', 'tmgs', 'tmhp', 'tmrg', 'tmsz', 'tmtp', 'tnar', 'tnfp', 'tnfpp', 'tnks',
          'tnksp', 'tnya', 'tnyap', 'tnzr', 'tnzrp', 'tomg', 'tomsp', 'toor', 'tozz', 'tpsb', 'trgm', 'trmzp', 'trnm',
          'trss', 'tses', 'tsgip', 'tstk', 'tsvs', 'ttmz', 'ttmzp', 'tupl', 'tvet', 'tvst', 'tvsx', 'txff', 'tyds',
          'typm', 'tzcz', 'tzep', 'tzepp', 'tzkmp', 'udrn', 'ufal', 'ugok', 'ugrb', 'uizk', 'uizkp', 'ulen', 'ulenp',
          'ungs', 'unmc', 'updt', 'upir', 'upirp', 'uppop', 'upsz', 'urag', 'uram', 'urbm', 'urelp', 'urpb', 'urrm',
          'usdb', 'utbnp', 'utst', 'uzem', 'uzrtp', 'vadr', 'vazzp', 'vfltp', 'vggg', 'vikr', 'vkof', 'vlgg', 'vmtp',
          'vnip', 'voad', 'vogz', 'vomdp', 'vonm', 'voos', 'vopt', 'vsnk', 'vspt', 'vstb', 'vvcr', 'yars', 'yarz',
          'yasn', 'yats', 'yazt', 'ymnp', 'yrog', 'yugs', 'yzda', 'zdeg', 'zepo', 'zkdb', 'zkre', 'zlad', 'zladp',
          'zmek', 'zmekp', 'zrzn', 'zsem', 'zsemp', 'zsgp', 'zsme', 'zstr', 'zstrp', 'zvmz', 'zvst', 'zzgtp', 'sempp',
          'smppp', 'tmeup', 'vorg', 'TNSE', 'OTCP', 'IRAO', 'IDVP', 'RUAL', 'SIBG', 'UWGN', 'GRNT', 'solr', 'rcco',
          'open', 'pskb', 'GAZAP', 'nfks', 'ESGR'}


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
                "/get_strategy <date(YYYY-MM-DD)>(from 2013-01-01) <MOEX code> <phase of day(OPEN/CLOSE)>(e.g. "
                "2021-10-14 YNDX OPEN) "
            )

        @self.bot.message_handler(commands=["get_strategy"])
        def getStrategyBot(message: telebot.types.Message):
            # reply to add_config command
            print("Received get_strategy message")

            if len(message.text.split()[1:]) < 3:
                self.bot.reply_to(
                    message,
                    "Not enough args"
                )
                return

            date, code, phase = message.text.split()[1:]

            if phase not in {"OPEN", "CLOSE"}:
                self.bot.reply_to(
                    message,
                    "Please choose phase of day correctly: OPEN/CLOSE"
                )
                return

            if datetime.strptime(date, "%Y-%m-%d") < datetime.strptime("2013-01-01", "%Y-%m-%d"):
                self.bot.reply_to(
                    message,
                    "Date is earlier than possible"
                )
                return

            if code not in stocks:
                self.bot.reply_to(
                    message,
                    "Code is not valid for MOEX"
                )
                return

            if not moex_api.check_date(date, code):
                self.bot.reply_to(
                    message,
                    "Cannot find date: {}.\nThis can happen if there were no trades on this date.\n(For example, the day was a weekend).\n".format(date)
                )
                return

            m = None
            d_m = None
            for i in self.trades_.process_request(date, code, phase):
                if i == '':
                    continue
                DAY, DAY_P, INCOME_IN_P_DAY, DAY_M, LOSS_IN_M_DAY, MONEY, MONEY_2 = i.split(',')
                if m is None:
                    m = float(MONEY_2)
                    d_m = DAY
                elif float(MONEY_2) > m:
                    m = float(MONEY_2)
                    d_m = DAY
                self.bot.reply_to(
                    message,
                    f"DAY: {DAY};\n"
                    f"% of DAY WITH +: {DAY_P};\n"
                    f"% of INCOME: {INCOME_IN_P_DAY};\n"
                    f"% of DAY WITH -: {DAY_M};\n"
                    f"% of LOSS: {LOSS_IN_M_DAY};\n"
                    f"TOTAL PUT: {MONEY};\n"
                    f"CURRENT PRICE: {MONEY_2}\n"
                )

            self.bot.reply_to(
                message,
                f"BEST DAY TO BUY: {d_m}"
            )

    def launchBot(self):
        # start polling
        print("Launching bot...")
        self.bot.polling()


if __name__ == "__main__":
    tbot = HaboobaBot()
    tbot.launchBot()
