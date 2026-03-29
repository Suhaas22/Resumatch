from rest_framework.decorators import api_view
from rest_framework.response import Response
from matcher.services.match_service import process_match
from .serializers import MatchResponseSerializer
from django.views.decorators.csrf import csrf_exempt



@api_view(['POST'])
def match_resume(request):

    resume = request.FILES.get("resume")
    job_description = request.data.get("job_description")

    if not resume:
        return Response({"error": "Resume is required"}, status=400)

    if not job_description:
        return Response({"error": "Job description is required"}, status=400)

    try:
        result = process_match(resume, job_description)
        serializer = MatchResponseSerializer(data = result)

        if serializer.is_valid():
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status = 400)

    except Exception as e:
        print("ERROR:", str(e))
        return Response({"error": str(e)}, status=400)




#   ---------------------------------------------

# model evaluation view

# @csrf_exempt
# def match_text(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST only"}, status=405)

#     resume_text = request.POST.get("resume_text", "").strip()
#     job_description = request.POST.get("job_description", "").strip()

#     if not resume_text:
#         return JsonResponse({"error": "resume_text is required"}, status=400)
#     if not job_description:
#         return JsonResponse({"error": "job_description is required"}, status=400)

#     # Call your existing scoring logic directly
#     # Replace these with whatever functions you already use
#     from .utils import extract_skills, compute_score  # adjust import to match your project
#     result = compute_score(resume_text, job_description)

#     return JsonResponse(result)