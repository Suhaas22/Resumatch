from rest_framework import serializers

class MatchResponseSerializer(serializers.Serializer):
    score = serializers.FloatField()

    skill_score = serializers.FloatField()
    text_score = serializers.FloatField()
    experience_score = serializers.FloatField()
    projects_score = serializers.FloatField()

    experience_years = serializers.FloatField()
    projects_count = serializers.IntegerField()

    resume_skills = serializers.ListField()
    matched_skills = serializers.ListField()
    missing_skills = serializers.ListField()

    suggestions = serializers.ListField()