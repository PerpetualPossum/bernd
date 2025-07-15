from peewee import SqliteDatabase, Model, CharField, IntegerField

from bernd.constants import DATABASE


class GuildSetting(Model):
    guild_id = IntegerField(primary_key=True)
    response_mode = CharField(default="single")
    chaos_level = IntegerField(default=1)

    class Meta:
        database = DATABASE
        table_name = "guild_settings"
