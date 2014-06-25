
# def draw(request,poll_id):
#     latest_poll_list = Lokalizacja.objects.all()[:poll_id]
#     context = {'locations': latest_poll_list}
#     return render(request, 'polls/wizualizacja.html', context)

# def drawCenters(request,user_id):
#     clustering.ClusterData(user_id)
#     latest_poll_list = Clusters.objects.filter(device_id=user_id)
#     context = {'locations': latest_poll_list}
#     return render(request, 'polls/clustersDraw.html', context)