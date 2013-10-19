from django.db import models


class Prop(models.Model):
    """
    A proposition on the 2012 California ballot.
    """
    name = models.CharField(max_length=10,
        help_text='The name of the proposition.')
    short_name = models.CharField(max_length=500)
    sec_state_id = models.CharField('Secretary of State ID', max_length=10, blank=True)
    objects = models.Manager()

    class Meta:
        app_label = 'contributions'
        ordering = ("name",)

    def __unicode__(self):
        return unicode("Proposition %s" % self.name)


class Campaign(models.Model):
    """
    Intermediary model between committees and props.
    
    Necessary because a committee can campaign for multiple
    propositions.
    """
    committee = models.ForeignKey("Committee")
    prop = models.ForeignKey("Prop")
    POSITION_CHOICES = (
        ('Support', 'Support'),
        ('Oppose', 'Oppose')
    )
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    
    class Meta:
        app_label = 'contributions'
    
    def __unicode__(self):
        return unicode("Campaign: %s %s" % (self.position, self.prop))


class Committee(models.Model):
    """
    A California campaign committee in the 2012 election.
    """
    name = models.CharField(max_length=500)
    sec_state_id = models.CharField(max_length=10)
    position = models.CharField(max_length=500, blank=True)
    has_multiple_campaigns = models.BooleanField(default=False)
    campaigns = models.ManyToManyField("Prop", through="Campaign")
    objects = models.Manager()
    
    class Meta:
        app_label = 'contributions'
        ordering = ("name",)
    
    def __unicode__(self):
        return unicode(self.name)


class Contribution(models.Model):
    """
    A finanical contribution made to a committee. A line-item.
    """
    name = models.CharField(max_length=500)
    city = models.CharField(max_length=500, blank=True)
    state = models.CharField(max_length=500, blank=True)
    zip_code = models.CharField(max_length=500, blank=True)
    employer = models.CharField(max_length=500, blank=True)
    occupation = models.CharField(max_length=500, blank=True)
    amount = models.FloatField()
    contribution_type = models.CharField(max_length=500, blank=True)
    transaction_date = models.DateField(blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    transaction_id = models.CharField(max_length=500)
    # On this, we'll see if we can match the committee ID from above
    # with anything we already have in the database. This should only be
    # used for committees donating to each other.
    sec_state_committee_id = models.CharField(max_length=500, blank=True,
        help_text='Filled in when a committee gives to another committee')
    from_committee = models.ForeignKey("Committee",
        related_name='from_committee', blank=True, null=True)
    # and this is the committee the contribution went to
    committee = models.ForeignKey("Committee")
    # CLEAN FIELDS
    clean_name = models.CharField(max_length=500, blank=True)
    clean_city = models.CharField(max_length=500, blank=True)
    clean_occupation = models.CharField(max_length=500, blank=True)
    clean_employer = models.CharField(max_length=500, blank=True)
    clean_location = models.CharField(max_length=500, blank=True)
    clean_state = models.CharField(max_length=500, blank=True)
    objects = models.Manager()

    class Meta:
        app_label = 'contributions'
        ordering = ("-amount", "-transaction_date")
    
    def __unicode__(self):
        return unicode(self.transaction_id)
