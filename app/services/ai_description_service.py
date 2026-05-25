import logging
import re
from dataclasses import dataclass
from decimal import Decimal

import google.generativeai as genai

from app.core.config import get_settings
from app.models.combustivel import Combustivel

logger = logging.getLogger(__name__)

MAX_DESCRIPTION_LENGTH = 200
FALLBACK_DESCRIPTION = "Veículo conservado, revisado e pronto para transferência."

COMBUSTIVEL_LABELS = {
    Combustivel.FLEX: "Flex",
    Combustivel.GASOLINA: "Gasolina",
    Combustivel.DIESEL: "Diesel",
    Combustivel.ELETRICO: "Elétrico",
    Combustivel.HIBRIDO: "Híbrido",
}


@dataclass(frozen=True)
class CarDescriptionContext:
    marca: str
    nome_modelo: str
    ano: int
    combustivel: Combustivel
    cor: str
    quilometragem: int
    num_portas: int
    valor_anuncio: Decimal
    valor_fipe: Decimal


class AIDescriptionService:
    def __init__(self) -> None:
        settings = get_settings()
        self._api_key = settings.gemini_api_key
        self._model_name = settings.gemini_model 

    def generate(self, context: CarDescriptionContext) -> str:
        if not self._api_key:
            logger.warning("GEMINI_API_KEY não configurada; usando fallback.")
            return self._fallback(context)

        try:
            genai.configure(api_key=self._api_key)
            model = genai.GenerativeModel(
                self._model_name,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                ),
            )
            response = model.generate_content(self._build_prompt(context))
            text = response.text if response.text else ""
            description = self._sanitize(text)
            if description:
                return description
        except Exception:
            logger.exception("Falha ao gerar descrição com Gemini")

        return self._fallback(context)

    def _build_prompt(self, context: CarDescriptionContext) -> str:
        combustivel = COMBUSTIVEL_LABELS.get(context.combustivel, context.combustivel.value)
        
        diferenca_fipe = context.valor_fipe - context.valor_anuncio
        info_fipe = ""
        if diferenca_fipe > 0:
            info_fipe = f"- Oportunidade: Este carro está R$ {diferenca_fipe:,.2f} ABAIXO da tabela FIPE!"

        return f"""Você é um vendedor de carros experiente no Brasil e trabalha criando anúncios para um site estilo Webmotors.
Escreva uma descrição de venda comercial, atraente e fluida usando os dados fornecidos.

Regras estritas:
1. Retorne APENAS o texto do anúncio, sem nenhuma introdução, aspas ou explicações.
2. O texto deve ter no MÁXIMO {MAX_DESCRIPTION_LENGTH} caracteres.
3. Não use emojis, tópicos, listas ou formatação Markdown.
4. Crie uma frase corrida, natural e vendedora. 
5. Você PODE (e deve) citar os dados do veículo de forma natural para valorizar o anúncio (ex: falar da cor, que tem 4 portas, exaltar a baixa quilometragem ou o preço).

Dados do veículo:
- Marca e Modelo: {context.marca} {context.nome_modelo}
- Ano: {context.ano}
- Combustível: {combustivel}
- Cor: {context.cor}
- Quilometragem: {context.quilometragem:,} km
- Portas: {context.num_portas}
- Valor do Anúncio: R$ {context.valor_anuncio:,.2f}
{info_fipe}

Exemplos de bom estilo para se inspirar:
- Excelente oportunidade! Corolla Flex em ótimo estado de conservação, com quilometragem baixa e preço especial abaixo da tabela FIPE. Perfeito para quem busca um sedã completo, confiável e econômico.
- Lindo veículo na cor prata, muito bem conservado e com ótimo desempenho. Uma oportunidade perfeita de levar um carro completo, espaçoso e ideal para o dia a dia. Venha conferir!

Descrição do Anúncio:"""

    def _sanitize(self, text: str) -> str:
        # Remove quebras de linha, aspas externas e limpa espaços extras
        cleaned = text.strip().strip("\"'")
        cleaned = cleaned.replace("\n", " ")
        cleaned = re.sub(r"[#*_`]", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned[:MAX_DESCRIPTION_LENGTH].strip()

    def _fallback(self, context: CarDescriptionContext) -> str:
        if context.valor_anuncio < context.valor_fipe:
            return "Excelente oportunidade! Veículo conservado e com preço abaixo da tabela FIPE. Aproveite!"[:MAX_DESCRIPTION_LENGTH]

        if context.quilometragem <= 40_000:
            return "Oportunidade! Veículo impecável, com baixa quilometragem, excelente estado e pronto para uso."[:MAX_DESCRIPTION_LENGTH]

        return FALLBACK_DESCRIPTION[:MAX_DESCRIPTION_LENGTH]