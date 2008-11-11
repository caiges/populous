from django.contrib import admin

class SportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}

class MatchAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Match Details'),
            {'fields': (('sport','gender'), 'game_time')
        }),
        (_('Scores'),
            {'fields': (('home_team', 'home_team_score'), ('away_team', 'away_team_score'))
        }),
    )
    list_filter = ('gender',)

admin.site.register(Sport, SportAdmin)
admin.site.register(Match, MatchAdmin)