import awesome.plugins.ask.data_source
import awesome.plugins.update.data_source
import awesome.util.repair_sqlite as sqlite

TB_NAME = 'fybot.db'
ASK_KEYWORD = awesome.plugins.ask.data_source.get_ask_keyword()
UPDATE_KEYWORD = awesome.plugins.update.data_source.get_update_keyword()
