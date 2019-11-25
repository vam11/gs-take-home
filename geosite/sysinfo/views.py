from django.shortcuts import render
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from geosite.sysinfo.serializers import SimpleRequestSerializer
from geosite.sysinfo.models import Request

import geosite.sysinfo.utilities as utils


class Index(APIView):
    def get(self, request):

        # Create a new entry in the `requests` table logging the request
        req_type = utils.get_req_type_from_rest_verb("GET")
        new_request = Request()
        new_request.req_type = req_type
        new_request.save()

        # TODO: improve this as this fetches all the entries and sorts them.
        # If the table has millions of rows, it might be better to execute
        # a custom database query
        # last_ten = Request.objects.all().order_by('req_date')
        last_ten = Request.objects.order_by('-req_date')[:10]

        for entry in last_ten:
            rest_verb = utils.get_rest_verb_from_req_type(req_type)
            entry.req_type = rest_verb

        cpu_info_out = utils.execute_cmd("cat /proc/cpuinfo")
        date_out = utils.execute_cmd("date")

        template_dict = {"last_10": last_ten, "cpu_info": cpu_info_out, "date": date_out}

        return render(request, 'sysinfo/index.html', template_dict)


class API(APIView):
    def get_object(self, pk):
        try:
            return Request.objects.get(id=pk)
        except Request.DoesNotExist:
            raise Http404

    def get(self, request, pk):

        request = self.get_object(pk)
        serializer = SimpleRequestSerializer(request)
        return Response(serializer.data)

    def post(self, request, pk):

        req = self.get_object(pk)
        serializer = SimpleRequestSerializer(req, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            entry_to_delete = Request.objects.get(id=pk)
        except Request.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        entry_to_delete.delete()
        return Response(status=status.HTTP_200_OK)
