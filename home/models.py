from django.db import models

class Type(models.Model):
    intitule = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.intitule


class Global(models.Model):
    societe = models.CharField(max_length=255)
    codetiers = models.CharField(max_length=255)
    intitule = models.CharField(max_length=255)
    tier = models.CharField(max_length=255)
    comptegeneral = models.CharField(max_length=255)

    def __str__(self):
        return self.societe



class Tier(models.Model):
    societe = models.CharField(max_length=255, default="Default")

    def __str__(self):
        return self.societe



class Societe(models.Model):
    TYPES = (
        ('sage100', 'Sage100'),
        ('x3v1', 'X3V1(AGRI)'),
        ('x3v2', 'X3V2(SMTP)')
    )

    name = models.CharField(max_length=150, unique=True, verbose_name='Nom du Société', null=True)
    user = models.CharField(max_length=150, default='reader', null=True)
    password = models.CharField(max_length=150, default='m1234', null=True)
    server = models.CharField(max_length=25, default='Srvi7dsiamb01', null=True)
    types = models.CharField(max_length=50, choices=TYPES, default="sage100")
    value = models.CharField(max_length=150, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.value and self.name:
            self.value = self.name
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name', 'active']

class AssociationSociete(models.Model):
    societe1 = models.ForeignKey(Societe, on_delete=models.CASCADE, verbose_name='Societe 1', related_name='societe1_associations')
    societe2 = models.ForeignKey(Societe, on_delete=models.CASCADE, verbose_name='Societe 2', related_name='societe2_associations')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Type de Transaction')
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Numéro Tier')

    def __str__(self):
        return f"{self.societe1.name} - {self.societe2.name}"

class Indentite(models.Model):
    name = models.CharField(max_length=250)
    correspondance = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Tableau(models.Model):
    base = models.CharField(max_length=50, blank=True)
    ecPiece = models.IntegerField()
    ecRefPiece = models.CharField(max_length=50)
    ecNo = models.IntegerField()

    def __str__(self):
        return self.base

class ListInterco(models.Model):
    interco = models.CharField(max_length=10, unique=True)
    societe1 = models.CharField(max_length=150, blank=True)
    ecpiece_tableau_1 = models.CharField(max_length=15, blank=True)
    societe2 = models.CharField(max_length=150, blank=True)
    ecpiece_tableau_2 = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.interco

class IntercoHistorique(models.Model):
    interco = models.CharField(max_length=10, blank=True)
    tableau1 = models.ForeignKey(Tableau, on_delete=models.CASCADE, related_name='historique_tableau1', blank=True, null=True)
    tableau2 = models.ForeignKey(Tableau, on_delete=models.CASCADE, related_name='historique_tableau2', blank=True, null=True)

    def __str__(self):
        return self.interco

    @classmethod
    def get_last_interco(cls):
        last_interco_obj = cls.objects.order_by('-id').first()
        return last_interco_obj.interco if last_interco_obj else None

class Transaction(models.Model):
    date = models.DateField()
    description = models.TextField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    societe1 = models.ForeignKey(Societe, related_name='transactions_societe1', on_delete=models.CASCADE)
    societe2 = models.ForeignKey(Societe, related_name='transactions_societe2', on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)



