from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from setores.models import Setor
from .models import Patrimonio, HistoricoPatrimonio


class PatrimonioModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.setor = Setor.objects.create(
            nome='TI', sigla='TI', secretaria='Administração'
        )
        cls.user = User.objects.create_user(
            username='teste', password='12345'
        )

    def test_numero_gerado_automaticamente(self):
        p = Patrimonio.objects.create(
            descricao='Computador Dell',
            setor=self.setor,
            responsavel=self.user,
        )
        self.assertIsNotNone(p.numero)
        self.assertTrue(p.numero.startswith('2026-'))

    def test_numero_unico(self):
        p1 = Patrimonio.objects.create(
            descricao='Monitor',
            setor=self.setor,
            responsavel=self.user,
        )
        p2 = Patrimonio.objects.create(
            descricao='Teclado',
            setor=self.setor,
            responsavel=self.user,
        )
        self.assertNotEqual(p1.numero, p2.numero)

    def test_soft_delete(self):
        p = Patrimonio.objects.create(
            descricao='Mouse',
            setor=self.setor,
            responsavel=self.user,
        )
        p.ativo = False
        p.save()
        self.assertFalse(Patrimonio.objects.filter(id=p.id, ativo=True).exists())
        self.assertTrue(Patrimonio.all_objects.filter(id=p.id).exists() if hasattr(Patrimonio, 'all_objects') else Patrimonio.objects.filter(id=p.id).exists())

    def test_historico_criacao(self):
        p = Patrimonio.objects.create(
            descricao='Impressora',
            setor=self.setor,
            responsavel=self.user,
        )
        # O historico e criado pela view, testamos o model direto
        h = HistoricoPatrimonio.objects.create(
            patrimonio=p,
            tipo_movimento=HistoricoPatrimonio.TipoMovimento.CRIACAO,
            descricao='Teste de historico',
            usuario=self.user,
            setor_novo=self.setor.nome,
            responsavel_nome=self.user.username,
            status_novo='Ativo',
        )
        self.assertEqual(h.patrimonio, p)
        self.assertEqual(h.tipo_movimento, 'criacao')

    def test_status_choices(self):
        p = Patrimonio.objects.create(
            descricao='Scanner',
            setor=self.setor,
            responsavel=self.user,
            status=Patrimonio.Status.MANUTENCAO,
        )
        self.assertEqual(p.status, 'manutencao')
        self.assertEqual(p.get_status_display(), 'Manutenção')

    def test_str_representation(self):
        p = Patrimonio.objects.create(
            descricao='Webcam',
            setor=self.setor,
            responsavel=self.user,
        )
        self.assertIn(p.numero, str(p))
        self.assertIn('Webcam', str(p))
