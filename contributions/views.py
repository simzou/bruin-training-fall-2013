import json
import logging

from django.db.models import Sum, Count
from django.views.generic import TemplateView
from contributions.models import Prop, Contribution


class IndexView(TemplateView):
    # tell our view which template to use
    template_name = "contributions/index.html"

    def get_context_data(self, **kwargs):
        # grab our context, so we can add to it
        context = super(IndexView, self).get_context_data(**kwargs)
        # get all of the props
        props = Prop.objects.all()
        # set up an empty data dictionary
        data = []
        # loop through all the props, and grab their totals
        for i in props:
            # grab the IDs of all the commitees that support the prop
            support_committees = i.campaign_set.filter(position='Support')\
                                    .values_list('committee_id', flat=True)
            # And all the committees that oppose it
            oppose_committees = i.campaign_set.filter(position='Oppose')\
                                    .values_list('committee_id', flat=True)
            # Then use those committee IDs to filter on the contributions
            # that either support or oppose the proposition.
            # Use the Django aggregate method to add them all up.
            data.append({
                'prop': i.name,
                'support': Contribution.objects.filter(committee_id__in=support_committees)\
                                .aggregate(sum=Sum('amount'))['sum'] or 0,
                'oppose': Contribution.objects.filter(committee_id__in=oppose_committees)\
                                .aggregate(sum=Sum('amount'))['sum'] or 0,
            })
        # put all of the values in a single list
        # so we can easily grab the max
        all_vals = []
        for i in data:
            all_vals.append(i['support'])
            all_vals.append(i['oppose'])

        # Here we can get a list of all of the unique contributor names
        # along with their total contributions
        contributors = Contribution.objects.values('clean_name')\
                    .annotate(contribs=Sum('amount')).order_by('-contribs')

        states = Contribution.objects.values('state')\
                    .annotate(contribs=Sum('amount')).order_by('-contribs')

        state_amounts = []
        for s in states[0:25]:
            state_amounts.append({
                'state': str(s['state']),
                'contribs': s['contribs']
            })

        contributor_list = []
        for c in contributors[0:10]:
            contributor_list.append({
                'name': c['clean_name'],
                'contribs': c['contribs']
            })
        context['state_amounts'] = state_amounts
        context['contributor_list'] = contributor_list
        context['contributors'] = enumerate(contributors[0:10], start=1)
        context['max_value'] = max(all_vals)
        context['summary_data'] = data
        context['summary_json'] = json.dumps(data)
        return context