# -*- coding: utf-8 -*-
"""
PORTUGUÊS DO BRASIL — CURSO COMPLETO A0–C1
Manual interactivo para hispanohablantes.

Contenido original organizado en 60 capítulos.
Incluye:
- objetivos
- vocabulario
- pronunciación orientativa
- gramática
- ejemplos
- diálogo
- lectura
- comprensión
- ejercicios
- práctica oral
- situación real
- errores típicos de hispanohablantes
- repaso
- evaluación
- respuestas
- registro de progreso

NOTA:
Este curso es material original. No reproduce literalmente libros comerciales.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import json
from pathlib import Path


# ============================================================
# MODELOS
# ============================================================

@dataclass
class Ejercicio:
    pregunta: str
    respuesta: str


@dataclass
class Capitulo:
    numero: int
    nivel: str
    titulo: str
    objetivo: str
    vocabulario: List[Tuple[str, str]]
    pronunciacion: List[Tuple[str, str]]
    gramatica: List[str]
    ejemplos: List[Tuple[str, str]]
    dialogo: List[Tuple[str, str]]
    lectura: str
    comprension: List[Ejercicio]
    ejercicios: List[Ejercicio]
    practica_oral: List[str]
    situacion_real: str
    errores_hispanohablantes: List[str]
    repaso: List[str]
    evaluacion: List[Ejercicio]


# ============================================================
# CONTENIDO BASE POR CAPÍTULO
# ============================================================

TEMAS = [
    # A0
    (1, "A0", "Primeiros passos", "Saludar, despedirse y usar fórmulas básicas de cortesía."),
    (2, "A0", "Quem é você?", "Presentarse y preguntar el nombre de otra persona."),
    (3, "A0", "De onde você é?", "Hablar del país de origen y la nacionalidad."),
    (4, "A0", "Minha família", "Presentar a la familia y expresar posesión."),
    (5, "A0", "Números e idade", "Decir la edad, números, teléfono y datos básicos."),
    (6, "A0", "Minha rotina", "Hablar de acciones habituales en presente."),
    (7, "A0", "Que horas são?", "Decir la hora, fechas y horarios."),
    (8, "A0", "Onde você mora?", "Hablar de vivienda, ubicación y direcciones."),
    (9, "A0", "Comida e bebida", "Pedir alimentos y expresar gustos."),
    (10, "A0", "Revisão A0", "Integrar y consolidar todo el nivel A0."),
    # A1
    (11, "A1", "Minha casa", "Describir habitaciones, muebles y ubicación."),
    (12, "A1", "Um dia normal", "Describir una rutina diaria con verbos frecuentes."),
    (13, "A1", "Gostos e preferências", "Expresar gustos, preferencias y opiniones simples."),
    (14, "A1", "Na cidade", "Moverse por la ciudad y usar contracciones frecuentes."),
    (15, "A1", "Compras e roupas", "Comprar ropa, preguntar precios y comparar."),
    (16, "A1", "No restaurante", "Pedir comida y resolver situaciones en un restaurante."),
    (17, "A1", "Saúde e corpo", "Describir síntomas y pedir ayuda médica básica."),
    (18, "A1", "Tempo livre", "Hablar de actividades, hobbies y frecuencia."),
    (19, "A1", "Viagens", "Hablar de transporte, hoteles y planes de viaje."),
    (20, "A1", "Revisão A1", "Integrar y consolidar todo el nivel A1."),
    # A2
    (21, "A2", "O que você fez ontem?", "Relatar hechos terminados en el pasado."),
    (22, "A2", "Minha infância", "Describir hábitos y situaciones del pasado."),
    (23, "A2", "Histórias do passado", "Combinar pretérito perfeito e imperfeito."),
    (24, "A2", "Planos para o futuro", "Expresar planes, intenciones y previsiones."),
    (25, "A2", "Trabalho e profissão", "Hablar del trabajo, responsabilidades y experiencia."),
    (26, "A2", "Estudos e aprendizagem", "Hablar de estudios, obligaciones y aprendizaje."),
    (27, "A2", "Relacionamentos", "Describir relaciones, personalidad y convivencia."),
    (28, "A2", "Brasil e cultura", "Hablar de costumbres y cultura brasileña."),
    (29, "A2", "Problemas cotidianos", "Explicar problemas y pedir soluciones."),
    (30, "A2", "Revisão A2", "Integrar y consolidar todo el nivel A2."),
    # B1
    (31, "B1", "Experiências de vida", "Relatar experiencias con mayor precisión temporal."),
    (32, "B1", "Contando histórias", "Narrar historias usando conectores."),
    (33, "B1", "Opiniões", "Expresar y justificar opiniones."),
    (34, "B1", "Conselhos e recomendações", "Dar consejos y recomendaciones."),
    (35, "B1", "Hipóteses", "Expresar condiciones e hipótesis reales."),
    (36, "B1", "Desejos e sentimentos", "Expresar deseos, emociones y subjetividad."),
    (37, "B1", "Trabalho e negócios", "Comunicarse en situaciones profesionales."),
    (38, "B1", "Notícias e sociedade", "Comprender noticias y reportar información."),
    (39, "B1", "Português brasileiro real", "Comprender expresiones frecuentes del habla."),
    (40, "B1", "Revisão B1", "Integrar y consolidar todo el nivel B1."),
    # B2
    (41, "B2", "Argumentação", "Construir argumentos claros y bien organizados."),
    (42, "B2", "Debates", "Debatir, matizar y contraargumentar."),
    (43, "B2", "Subjuntivo avançado", "Usar varios tiempos del subjuntivo con precisión."),
    (44, "B2", "Condições e hipóteses", "Expresar hipótesis complejas y contrafactuales."),
    (45, "B2", "Português formal", "Adaptar el registro según la situación."),
    (46, "B2", "Escrita profissional", "Redactar emails e informes profesionales."),
    (47, "B2", "Mídia brasileira", "Comprender lenguaje periodístico y audiovisual."),
    (48, "B2", "Expressões idiomáticas", "Usar expresiones idiomáticas frecuentes."),
    (49, "B2", "Conversação natural", "Hablar con mayor ritmo y cohesión."),
    (50, "B2", "Revisão B2", "Integrar y consolidar todo el nivel B2."),
    # C1
    (51, "C1", "Nuances da língua", "Comprender diferencias finas de significado."),
    (52, "C1", "Português coloquial avançado", "Interpretar habla coloquial compleja."),
    (53, "C1", "Expressões e gírias", "Comprender y usar jerga según contexto."),
    (54, "C1", "Argumentação avançada", "Argumentar con precisión, matices y evidencia."),
    (55, "C1", "Português acadêmico", "Leer y producir textos académicos."),
    (56, "C1", "Português profissional", "Negociar y presentar ideas profesionalmente."),
    (57, "C1", "Textos complexos", "Interpretar textos densos y abstractos."),
    (58, "C1", "Comunicação avançada", "Comprender ironía, humor e implicaturas."),
    (59, "C1", "Fluência brasileira", "Mejorar naturalidad, ritmo y precisión."),
    (60, "C1", "Avaliação final C1", "Demostrar dominio global del curso A0–C1."),
]


VOCAB = {
1:[("olá","hola"),("oi","hola / hola informal"),("bom dia","buenos días"),("boa tarde","buenas tardes"),("boa noite","buenas noches"),("tchau","chau"),("por favor","por favor"),("obrigado/obrigada","gracias")],
2:[("eu","yo"),("você","tú / usted"),("ele","él"),("ela","ella"),("nome","nombre"),("ser","ser"),("chamar-se","llamarse"),("prazer","mucho gusto")],
3:[("Brasil","Brasil"),("Peru","Perú"),("brasileiro","brasileño"),("peruano","peruano"),("país","país"),("cidade","ciudad"),("de onde","de dónde"),("morar","vivir / residir")],
4:[("mãe","madre"),("pai","padre"),("irmão","hermano"),("irmã","hermana"),("filho","hijo"),("filha","hija"),("marido","esposo"),("esposa","esposa")],
5:[("zero","cero"),("dez","diez"),("vinte","veinte"),("cem","cien"),("idade","edad"),("telefone","teléfono"),("número","número"),("anos","años")],
6:[("acordar","despertarse"),("trabalhar","trabajar"),("estudar","estudiar"),("comer","comer"),("beber","beber"),("dormir","dormir"),("começar","empezar"),("terminar","terminar")],
7:[("hora","hora"),("hoje","hoy"),("amanhã","mañana"),("ontem","ayer"),("segunda-feira","lunes"),("mês","mes"),("ano","año"),("data","fecha")],
8:[("casa","casa"),("apartamento","departamento"),("rua","calle"),("bairro","barrio"),("perto","cerca"),("longe","lejos"),("direita","derecha"),("esquerda","izquierda")],
9:[("água","agua"),("café","café"),("arroz","arroz"),("feijão","frijoles"),("carne","carne"),("frango","pollo"),("pão","pan"),("suco","jugo")],
10:[("revisão","repaso"),("pergunta","pregunta"),("resposta","respuesta"),("frase","frase"),("texto","texto"),("ouvir","escuchar"),("falar","hablar"),("escrever","escribir")],
11:[("quarto","dormitorio"),("sala","sala"),("cozinha","cocina"),("banheiro","baño"),("mesa","mesa"),("cadeira","silla"),("cama","cama"),("janela","ventana")],
12:[("levantar","levantarse"),("tomar banho","bañarse"),("almoçar","almorzar"),("jantar","cenar"),("voltar","volver"),("sair","salir"),("fazer","hacer"),("ir","ir")],
13:[("gostar","gustar"),("adorar","encantar"),("preferir","preferir"),("achar","opinar / encontrar"),("música","música"),("filme","película"),("esporte","deporte"),("livro","libro")],
14:[("banco","banco"),("mercado","mercado"),("farmácia","farmacia"),("praça","plaza"),("ônibus","autobús"),("metrô","metro"),("esquina","esquina"),("avenida","avenida")],
15:[("camisa","camisa"),("calça","pantalón"),("sapato","zapato"),("tamanho","talla"),("preço","precio"),("barato","barato"),("caro","caro"),("experimentar","probarse")],
16:[("cardápio","menú"),("garçom","mesero"),("conta","cuenta"),("prato","plato"),("sobremesa","postre"),("entrada","entrada"),("pedir","pedir"),("trazer","traer")],
17:[("cabeça","cabeza"),("garganta","garganta"),("estômago","estómago"),("dor","dolor"),("febre","fiebre"),("remédio","medicamento"),("médico","médico"),("hospital","hospital")],
18:[("jogar","jugar"),("correr","correr"),("viajar","viajar"),("cozinhar","cocinar"),("dançar","bailar"),("sempre","siempre"),("às vezes","a veces"),("nunca","nunca")],
19:[("passagem","pasaje"),("aeroporto","aeropuerto"),("hotel","hotel"),("reserva","reserva"),("mala","maleta"),("voo","vuelo"),("embarque","embarque"),("chegada","llegada")],
20:[("revisar","repasar"),("praticar","practicar"),("compreender","comprender"),("responder","responder"),("descrever","describir"),("comparar","comparar"),("planejar","planificar"),("conversar","conversar")],
21:[("fui","fui"),("fiz","hice"),("comi","comí"),("vi","vi"),("cheguei","llegué"),("saí","salí"),("comprei","compré"),("aconteceu","ocurrió")],
22:[("infância","infancia"),("quando","cuando"),("brincar","jugar"),("morava","vivía"),("estudava","estudiaba"),("era","era"),("tinha","tenía"),("costumava","solía")],
23:[("enquanto","mientras"),("de repente","de repente"),("naquele dia","aquel día"),("primeiro","primero"),("depois","después"),("então","entonces"),("finalmente","finalmente"),("acontecimento","acontecimiento")],
24:[("plano","plan"),("projeto","proyecto"),("pretender","pretender"),("viajarei","viajaré"),("farei","haré"),("vou fazer","voy a hacer"),("talvez","quizá"),("esperar","esperar")],
25:[("emprego","empleo"),("empresa","empresa"),("chefe","jefe"),("colega","colega"),("salário","salario"),("experiência","experiencia"),("currículo","currículum"),("entrevista","entrevista")],
26:[("curso","curso"),("aula","clase"),("prova","examen"),("tarefa","tarea"),("aprender","aprender"),("precisar","necesitar"),("dever","deber"),("ter que","tener que")],
27:[("amizade","amistad"),("relacionamento","relación"),("gentil","amable"),("calmo","tranquilo"),("sincero","sincero"),("confiar","confiar"),("respeitar","respetar"),("conviver","convivir")],
28:[("cultura","cultura"),("costume","costumbre"),("festa","fiesta"),("carnaval","carnaval"),("samba","samba"),("comida típica","comida típica"),("região","región"),("diversidade","diversidad")],
29:[("problema","problema"),("quebrado","roto"),("atrasado","retrasado"),("perdido","perdido"),("resolver","resolver"),("ajuda","ayuda"),("reclamar","reclamar"),("consertar","reparar")],
30:[("consolidar","consolidar"),("narrar","narrar"),("explicar","explicar"),("opinar","opinar"),("solicitar","solicitar"),("relatar","relatar"),("organizar","organizar"),("avaliar","evaluar")],
31:[("experiência","experiencia"),("já","ya"),("ainda","todavía"),("nunca","nunca"),("recentemente","recientemente"),("desde","desde"),("durante","durante"),("lembrança","recuerdo")],
32:[("história","historia"),("enredo","trama"),("personagem","personaje"),("começo","inicio"),("meio","medio"),("fim","fin"),("porém","sin embargo"),("portanto","por lo tanto")],
33:[("opinião","opinión"),("concordar","estar de acuerdo"),("discordar","discrepar"),("argumento","argumento"),("motivo","motivo"),("ponto de vista","punto de vista"),("na minha opinião","en mi opinión"),("por outro lado","por otro lado")],
34:[("conselho","consejo"),("recomendação","recomendación"),("deveria","debería"),("poderia","podría"),("melhor","mejor"),("evitar","evitar"),("sugerir","sugerir"),("vale a pena","vale la pena")],
35:[("se","si"),("caso","en caso de que"),("quando","cuando"),("hipótese","hipótesis"),("condição","condición"),("possível","posible"),("provável","probable"),("resultado","resultado")],
36:[("desejo","deseo"),("esperança","esperanza"),("alegria","alegría"),("medo","miedo"),("surpresa","sorpresa"),("tomara","ojalá"),("querer que","querer que"),("esperar que","esperar que")],
37:[("negócio","negocio"),("reunião","reunión"),("cliente","cliente"),("prazo","plazo"),("orçamento","presupuesto"),("proposta","propuesta"),("contrato","contrato"),("negociar","negociar")],
38:[("notícia","noticia"),("jornal","periódico"),("reportagem","reportaje"),("fonte","fuente"),("segundo","según"),("afirmar","afirmar"),("divulgar","divulgar"),("acontecimento","acontecimiento")],
39:[("beleza","vale / todo bien"),("pois é","pues sí"),("cara","tipo / amigo"),("legal","genial"),("valeu","gracias / vale"),("tá","está"),("pra","para"),("né","¿no?")],
40:[("fluência","fluidez"),("coesão","cohesión"),("clareza","claridad"),("precisão","precisión"),("contexto","contexto"),("registro","registro"),("interação","interacción"),("autonomia","autonomía")],
41:[("tese","tesis"),("evidência","evidencia"),("premissa","premisa"),("conclusão","conclusión"),("sustentar","sostener"),("refutar","refutar"),("coerente","coherente"),("relevante","relevante")],
42:[("debate","debate"),("contraponto","contrapunto"),("ressalva","salvedad"),("discordância","desacuerdo"),("persuadir","persuadir"),("ponderar","ponderar"),("entretanto","sin embargo"),("ainda assim","aun así")],
43:[("subjuntivo","subjuntivo"),("embora","aunque"),("para que","para que"),("mesmo que","aunque"),("antes que","antes de que"),("desde que","siempre que"),("duvidar","dudar"),("supor","suponer")],
44:[("contrafactual","contrafactual"),("teria","habría"),("fosse","fuera"),("tivesse","tuviera"),("seria","sería"),("aconteceria","ocurriría"),("desde que","con tal de que"),("a menos que","a menos que")],
45:[("registro","registro"),("formal","formal"),("informal","informal"),("prezado","estimado"),("solicito","solicito"),("encaminhar","remitir"),("atenciosamente","atentamente"),("cordialmente","cordialmente")],
46:[("relatório","informe"),("anexo","adjunto"),("assunto","asunto"),("destinatário","destinatario"),("objetivo","objetivo"),("resultado","resultado"),("pendência","pendiente"),("providência","medida")],
47:[("manchete","titular"),("editorial","editorial"),("entrevista","entrevista"),("transmissão","transmisión"),("audiência","audiencia"),("viés","sesgo"),("apuração","verificación periodística"),("cobertura","cobertura")],
48:[("dar conta","lograr / poder con"),("ficar de olho","estar atento"),("quebrar o galho","sacar de apuros"),("puxar assunto","iniciar conversación"),("cair a ficha","darse cuenta"),("mão na massa","manos a la obra"),("fazer sentido","tener sentido"),("sem pé nem cabeça","sin sentido")],
49:[("aliás","por cierto"),("enfim","en fin"),("inclusive","incluso"),("tipo","tipo / como"),("quer dizer","es decir"),("na verdade","en realidad"),("ao mesmo tempo","al mismo tiempo"),("por sinal","por cierto")],
50:[("domínio","dominio"),("argumentação","argumentación"),("registro","registro"),("naturalidade","naturalidad"),("compreensão","comprensión"),("produção","producción"),("estratégia","estrategia"),("desempenho","desempeño")],
51:[("nuance","matiz"),("sutil","sutil"),("implícito","implícito"),("conotação","connotación"),("ambiguidade","ambigüedad"),("adequado","adecuado"),("preciso","preciso"),("contextual","contextual")],
52:[("coloquial","coloquial"),("redução","reducción"),("entonação","entonación"),("ritmo","ritmo"),("marcador discursivo","marcador discursivo"),("interjeição","interjección"),("subentendido","sobreentendido"),("espontâneo","espontáneo")],
53:[("gíria","jerga"),("regionalismo","regionalismo"),("expressão","expresión"),("contexto","contexto"),("geração","generación"),("grupo social","grupo social"),("adequação","adecuación"),("conotação","connotación")],
54:[("pressuposto","supuesto"),("inferência","inferencia"),("contradição","contradicción"),("consistência","consistencia"),("ressalva","salvedad"),("qualificar","matizar"),("fundamentar","fundamentar"),("sintetizar","sintetizar")],
55:[("resumo","resumen"),("introdução","introducción"),("metodologia","metodología"),("resultado","resultado"),("discussão","discusión"),("referência","referencia"),("citação","cita"),("hipótese","hipótesis")],
56:[("negociação","negociación"),("concessão","concesión"),("contrapartida","contrapartida"),("meta","meta"),("indicador","indicador"),("stakeholder","parte interesada"),("alinhamento","alineamiento"),("decisão","decisión")],
57:[("abstrato","abstracto"),("ensaio","ensayo"),("tese","tesis"),("metáfora","metáfora"),("estrutura","estructura"),("interpretação","interpretación"),("perspectiva","perspectiva"),("complexidade","complejidad")],
58:[("ironia","ironía"),("sarcasmo","sarcasmo"),("humor","humor"),("duplo sentido","doble sentido"),("implicatura","implicatura"),("intenção","intención"),("tom","tono"),("contexto","contexto")],
59:[("fluência","fluidez"),("prosódia","prosodia"),("cadência","cadencia"),("precisão","precisión"),("espontaneidade","espontaneidad"),("autocorreção","autocorrección"),("paráfrase","paráfrasis"),("naturalidade","naturalidad")],
60:[("avaliação","evaluación"),("desempenho","desempeño"),("competência","competencia"),("produção oral","producción oral"),("produção escrita","producción escrita"),("compreensão","comprensión"),("projeto final","proyecto final"),("autonomia","autonomía")],
}


GRAMATICA = {
1:["En portugués brasileño, los saludos cambian según el momento del día: bom dia, boa tarde, boa noite.",
   "Obrigado lo usa normalmente un hablante masculino; obrigada, una hablante femenina."],
2:["Pronombres básicos: eu, você, ele, ela, nós, vocês, eles, elas.",
   "Presente de ser: eu sou, você/ele/ela é, nós somos, vocês/eles/elas são."],
3:["Para origen: Sou do Peru. Sou de Lima. Para nacionalidad: Sou peruano/peruana.",
   "La contracción de + o = do y de + a = da."],
4:["Posesivos frecuentes: meu/minha, seu/sua, nosso/nossa.",
   "Los sustantivos y adjetivos suelen concordar en género y número."],
5:["Para la edad se usa ter: Eu tenho 30 anos. No se usa ser como en inglés.",
   "Números compuestos: vinte e um, trinta e dois, quarenta e cinco."],
6:["Verbos regulares: falar→falo, comer→como, abrir→abro.",
   "En portugués brasileño, você usa normalmente la forma de tercera persona."],
7:["Hora: É uma hora. São duas horas. Para minutos: São duas e quinze.",
   "Fechas: Hoje é oito de agosto. Dias de semana suelen llevar feira excepto sábado y domingo."],
8:["Estar expresa ubicación: Estou em casa. Morar expresa residencia: Moro em Lima.",
   "Preposiciones y contracciones: em + o = no; em + a = na."],
9:["Gostar exige de: gosto de café. Querer no presente: quero, quer, queremos, querem.",
   "Para pedir cortésmente: Eu gostaria de... / Pode me trazer...?" ],
10:["Repasa ser, estar, ter, morar, gostar y verbos regulares del presente.",
    "Integra preguntas con quem, onde, quando, quanto y como."],
11:["Há y tem pueden indicar existencia en el habla: Há uma mesa / Tem uma mesa.",
    "Ubicación: em cima de, embaixo de, ao lado de, perto de, longe de."],
12:["Verbos irregulares frecuentes: faço, vou, venho, tenho, saio.",
    "Marcadores de rutina: sempre, geralmente, às vezes, raramente, nunca."],
13:["Gostar de + sustantivo/infinitivo: gosto de música; gosto de viajar.",
    "Comparativos: mais... que/do que; menos... que/do que; tão... quanto."],
14:["Contracciones: de+o=do, de+a=da, em+o=no, em+a=na, a+o=ao.",
    "Imperativos útiles: vire, siga, atravesse, pegue."],
15:["Demostrativos: este/esta, esse/essa, aquele/aquela.",
    "Comparación: mais barato, menos caro, melhor, pior."],
16:["Pedir: Eu queria..., Eu gostaria de..., Pode trazer...?",
    "Pronombres de cortesía y expresiones: por favor, com licença, obrigado."],
17:["Estar com + síntoma: estou com febre, estou com dor de cabeça.",
    "Imperativo básico: tome, descanse, evite, procure."],
18:["Frecuencia: todos os dias, uma vez por semana, de vez em quando.",
    "Gostar/preferir + infinitivo para actividades."],
19:["Futuro próximo: ir + infinitivo: vou viajar, vamos ficar.",
    "Preposiciones de movimiento: para, até, de, por."],
20:["Integra presente, futuro próximo, comparativos, contracciones e imperativo básico.",
    "Practica diálogos completos de ciudad, compras, restaurante, salud y viaje."],
21:["Pretérito perfeito: falei, comi, abri; ir→fui; fazer→fiz; ver→vi.",
    "Se usa para acciones terminadas: Ontem trabalhei até tarde."],
22:["Pretérito imperfeito: falava, comia, abria; ser→era; ter→tinha.",
    "Se usa para hábitos, descripciones y acciones en progreso del pasado."],
23:["Perfecto para evento puntual; imperfecto para contexto: Eu dormia quando o telefone tocou.",
    "Conectores narrativos: enquanto, de repente, então, depois, finalmente."],
24:["Futuro próximo para planes: vou estudar. Futuro simple: estudarei.",
    "Talvez puede requerir subjuntivo en niveles más avanzados; aquí se trabaja comprensión básica."],
25:["Ter que, precisar de/precisar + infinitivo y dever expresan obligación o necesidad.",
    "Experiencia profesional puede narrarse combinando presente y pasado."],
26:["Dever + infinitivo expresa deber o recomendación; ter que expresa obligación más directa.",
    "Precisar de + sustantivo; precisar + infinitivo."],
27:["Pronombres objeto frecuentes en uso brasileño: me, te, se, nos.",
    "Adjetivos describen personalidad y concuerdan cuando corresponde."],
28:["Se trabaja principalmente comunicación intercultural y comparación.",
    "Conectores simples: além disso, por isso, porém, também."],
29:["Para problemas: não funciona, está quebrado, perdi..., preciso de ajuda.",
    "Pedidos educados: Você poderia...? Seria possível...?" ],
30:["Repasa pasado, futuro, obligaciones, conectores y estrategias de interacción.",
    "Combina descripción, narración y solicitud de ayuda."],
31:["Marcadores temporales: já, ainda, nunca, desde, há, durante.",
    "Contraste entre experiências terminadas y situaciones que continúan."],
32:["Narración cohesionada con primeiro, depois, enquanto, porém, por isso, finalmente.",
    "Alternancia de tiempos pasados para fondo y eventos."],
33:["Estructuras: acho que, acredito que, na minha opinião, concordo porque...",
    "Conectores argumentativos: além disso, porém, por outro lado, portanto."],
34:["Condicional: eu faria, você poderia, seria melhor.",
    "Consejo: se eu fosse você..., você deveria..., vale a pena..." ],
35:["Futuro do subjuntivo tras se/quando: se eu tiver, quando você chegar.",
    "Estructura real: Se eu tiver tempo, vou estudar."],
36:["Presente do subjuntivo: que eu fale, que você faça, que ele seja.",
    "Se usa tras deseo, duda, emoción y ciertas conjunciones."],
37:["Registro profesional: poderia enviar..., gostaria de confirmar..., conforme combinado...",
    "Diferencia entre lenguaje directo e indirecto según jerarquía y contexto."],
38:["Discurso indirecto: Ele disse que iria... / Segundo a reportagem...",
    "Distingue hecho, opinión, fuente y atribución."],
39:["En habla brasileña son comunes reducciones como tá, tô, pra, cê, né.",
    "Estas formas son muy comunes oralmente, pero no siempre adecuadas en escritura formal."],
40:["Integra narración, opinión, consejo, hipótesis, subjuntivo y registro.",
    "Objetivo: producir discurso conectado y comprensible de varios minutos."],
41:["Argumentación: tesis + evidencia + explicación + conclusión.",
    "Conectores: em primeiro lugar, além disso, contudo, portanto, em síntese."],
42:["Matización: concordo em parte; entendo o ponto, mas...; ainda assim...",
    "Contraargumentación debe responder a la idea, no a la persona."],
43:["Presente: espero que seja. Imperfeito: se fosse. Futuro: quando for.",
    "Conjunciones como embora, para que, mesmo que suelen activar subjuntivo."],
44:["Hipótesis contrafactual: Se eu tivesse sabido, teria agido diferente.",
    "Condiciones: desde que, contanto que, a menos que."],
45:["Formalidad léxica y sintáctica depende del destinatario y propósito.",
    "Evita coloquialismos en documentos formales salvo cita o efecto deliberado."],
46:["Un email profesional debe tener asunto claro, saludo, propósito, acción esperada y cierre.",
    "Informes usan estructura: contexto, objetivo, hallazgos, análisis, conclusión y acción."],
47:["Lenguaje periodístico distingue titular, lead, cuerpo, fuente y contexto.",
    "Evalúa sesgo, selección léxica y confiabilidad de la fuente."],
48:["Las expresiones idiomáticas no deben traducirse literalmente.",
    "El contexto determina significado, tono y registro."],
49:["Marcadores discursivos organizan el habla: aliás, enfim, na verdade, quer dizer.",
    "Naturalidad no significa hablar rápido, sino conectar ideas con claridad."],
50:["Integra argumentos, subjuntivo, condicionales, formalidad y expresiones idiomáticas.",
    "Producción B2 debe mostrar control de registro y cohesión."],
51:["Sinónimos cercanos pueden diferir en tono, intensidad o contexto.",
    "Analiza denotación, connotación e intención pragmática."],
52:["El habla avanzada incluye elipsis, reducciones, autocorrecciones y marcadores discursivos.",
    "La entonación puede cambiar el sentido pragmático de una frase."],
53:["La jerga depende de edad, región, comunidad y situación.",
    "Usarla bien exige comprender registro y posibles connotaciones."],
54:["Argumentar a nivel C1 implica anticipar objeciones y reconocer límites.",
    "Usa hedging: em certa medida, ao que tudo indica, é plausível que..." ],
55:["Escritura académica exige claridad, cohesión, fuentes y distinción entre evidencia e interpretación.",
    "Evita afirmaciones absolutas cuando la evidencia no las sostiene."],
56:["Negociación: posición, interés, concesión, contrapartida y cierre.",
    "Presentaciones profesionales deben señalar objetivo, datos, implicaciones y decisión."],
57:["Textos complejos requieren identificar tesis, estructura, presupuestos y recursos retóricos.",
    "Parafrasear demuestra comprensión sin copiar el original."],
58:["Ironía y humor dependen de contexto, conocimiento compartido y tono.",
    "Una frase puede significar pragmáticamente lo contrario de su contenido literal."],
59:["Fluidez avanzada combina precisión, ritmo, conectores, paráfrasis y autocorrección.",
    "La meta no es eliminar el acento, sino comunicarse con naturalidad y claridad."],
60:["Evaluación integral: comprensión, conversación, narración, argumentación y escritura.",
    "El proyecto final debe demostrar autonomía comunicativa en portugués brasileño."],
}


PRON = {
"olá":"o-LÁ", "oi":"ói", "bom dia":"bon DJÍ-a", "boa tarde":"BÔ-a TAR-dji",
"boa noite":"BÔ-a NÔI-tchi", "tchau":"chau", "obrigado/obrigada":"o-bri-GÁ-du / o-bri-GÁ-da",
"você":"vo-SÊ", "não":"nãu", "muito":"MŨI-tu", "gente":"ZHEN-tchi",
"cidade":"si-DÁ-dji", "noite":"NÔI-tchi", "dia":"DJÍ-a", "tarde":"TAR-dji",
"trabalho":"tra-BÁ-lyu", "filho":"FÍ-lyu", "mulher":"mu-LYÉR", "melhor":"me-LYÓR",
"hoje":"Ô-zhi", "amanhã":"a-ma-NYÃ", "pão":"pãu", "mãe":"mãi",
"irmão":"ir-MÃU", "coração":"ko-ra-SÃU", "Brasil":"bra-ZÍU", "português":"por-tu-GUÊS"
}


def pronunciacion_para(vocabulario):
    salida = []
    for pt, _ in vocabulario:
        if pt in PRON:
            salida.append((pt, PRON[pt]))
    if len(salida) < 4:
        # Reglas generales útiles como complemento
        reglas = [
            ("nh", "suena parecido a 'ñ': manhã"),
            ("lh", "sonido palatal, parecido a 'lli': filho"),
            ("ão", "sonido nasal: pão, irmão"),
            ("d + i / t + i", "en gran parte de Brasil puede sonar 'dji' / 'tchi'")
        ]
        for item in reglas:
            if item not in salida:
                salida.append(item)
            if len(salida) >= 4:
                break
    return salida


def ejemplos_para(n, vocab):
    palabras = [x[0] for x in vocab]
    if n <= 10:
        return [
            (f"Eu uso a palavra '{palabras[0]}' em uma frase simples.", f"Uso la palabra «{palabras[0]}» en una frase simple."),
            (f"Você conhece a palavra '{palabras[1]}'?", f"¿Conoces la palabra «{palabras[1]}»?"),
            (f"Hoje vamos praticar '{palabras[2]}'.", f"Hoy vamos a practicar «{palabras[2]}»."),
            (f"Eu quero aprender português todos os dias.", "Quiero aprender portugués todos los días.")
        ]
    elif n <= 30:
        return [
            (f"Ontem eu usei '{palabras[0]}' numa conversa.", f"Ayer usé «{palabras[0]}» en una conversación."),
            (f"É importante compreender '{palabras[1]}' no contexto.", f"Es importante comprender «{palabras[1]}» en contexto."),
            ("Eu consigo explicar a situação com mais detalhes.", "Puedo explicar la situación con más detalles."),
            ("Se eu tiver dúvida, vou perguntar em português.", "Si tengo una duda, preguntaré en portugués.")
        ]
    elif n <= 50:
        return [
            (f"O termo '{palabras[0]}' aparece com frequência neste contexto.", f"El término «{palabras[0]}» aparece con frecuencia en este contexto."),
            ("Na minha opinião, a clareza é tão importante quanto a precisão.", "En mi opinión, la claridad es tan importante como la precisión."),
            ("Embora existam opiniões diferentes, podemos comparar os argumentos.", "Aunque existan opiniones distintas, podemos comparar los argumentos."),
            ("Se analisarmos os dados com cuidado, chegaremos a uma conclusão melhor.", "Si analizamos los datos con cuidado, llegaremos a una conclusión mejor.")
        ]
    else:
        return [
            (f"A palavra '{palabras[0]}' exige atenção às nuances do contexto.", f"La palabra «{palabras[0]}» exige atención a los matices del contexto."),
            ("A interpretação mais adequada depende não apenas das palavras, mas também da intenção do falante.", "La interpretación más adecuada depende no solo de las palabras, sino también de la intención del hablante."),
            ("Ainda que a hipótese pareça plausível, convém reconhecer suas limitações.", "Aunque la hipótesis parezca plausible, conviene reconocer sus limitaciones."),
            ("Uma comunicação madura combina precisão lexical, coesão e sensibilidade ao registro.", "Una comunicación madura combina precisión léxica, cohesión y sensibilidad al registro.")
        ]


def dialogo_para(n, titulo, vocab):
    a, b, c = vocab[0][0], vocab[1][0], vocab[2][0]
    if n <= 10:
        return [
            ("A", f"Olá! Hoje vamos falar sobre {titulo.lower()}."),
            ("B", f"Ótimo. Eu já conheço '{a}', mas quero aprender '{b}'."),
            ("A", f"Sem problema. Vamos praticar também '{c}'."),
            ("B", "Perfeito. Podemos começar?")
        ]
    elif n <= 30:
        return [
            ("A", f"Você já teve alguma experiência relacionada a {titulo.lower()}?"),
            ("B", f"Sim. Eu me lembro de uma situação em que usei '{a}'."),
            ("A", f"E como você explicaria '{b}' nesse contexto?"),
            ("B", f"Eu explicaria usando um exemplo e depois compararia com '{c}'.")
        ]
    elif n <= 50:
        return [
            ("A", f"Qual é a sua opinião sobre o tema '{titulo}'?"),
            ("B", f"Eu começaria definindo '{a}' e apresentando evidências."),
            ("A", f"Mas alguém poderia discordar usando o argumento '{b}'."),
            ("B", f"É verdade. Nesse caso, eu faria uma ressalva e retomaria '{c}'.")
        ]
    else:
        return [
            ("A", f"Que nuance você considera mais importante em '{titulo}'?"),
            ("B", f"Depende do contexto. O termo '{a}' pode assumir sentidos diferentes."),
            ("A", f"Como evitar uma interpretação simplista de '{b}'?"),
            ("B", f"Comparando fontes, intenção, registro e a relação com '{c}'.")
        ]


def leitura_para(n, titulo, vocab):
    palavras = ", ".join([x[0] for x in vocab[:5]])
    if n <= 10:
        return (f"Hoje estudo o tema '{titulo}'. Aprendo palavras como {palavras}. "
                "Leio frases curtas, repito em voz alta e tento usar cada palavra em uma situação simples. "
                "Meu objetivo é entender antes de falar rápido. Todos os dias pratico um pouco.")
    elif n <= 20:
        return (f"Aprender '{titulo}' ajuda a resolver situações reais do cotidiano. "
                f"Nesta unidade aparecem palavras como {palavras}. "
                "O estudante observa exemplos, compara formas parecidas com o espanhol e pratica diálogos. "
                "Depois, cria frases próprias e tenta falar sem traduzir cada palavra.")
    elif n <= 30:
        return (f"No tema '{titulo}', o estudante aprende a combinar vocabulário e estruturas para falar com mais autonomia. "
                f"Entre os termos trabalhados estão {palavras}. "
                "A prática inclui compreender contexto, relatar experiências, pedir informação e justificar escolhas. "
                "O foco deixa de ser apenas reconhecer palavras e passa a ser produzir mensagens completas.")
    elif n <= 40:
        return (f"O domínio de '{titulo}' exige organização de ideias e atenção ao contexto. "
                f"Palavras como {palavras} ajudam a construir discursos mais claros. "
                "O estudante aprende a conectar acontecimentos, expressar opinião, reconhecer diferentes pontos de vista "
                "e ajustar o que diz conforme a reação do interlocutor.")
    elif n <= 50:
        return (f"Em '{titulo}', a língua é usada para analisar, argumentar e adaptar o registro. "
                f"Termos como {palavras} aparecem em situações que exigem precisão. "
                "Uma resposta eficaz não depende apenas de gramática correta: ela precisa apresentar relação lógica entre ideias, "
                "vocabulário adequado e consciência de quem está ouvindo ou lendo.")
    else:
        return (f"No nível avançado, '{titulo}' é estudado como parte de uma competência comunicativa ampla. "
                f"Conceitos como {palavras} são analisados não apenas pelo significado literal, mas também por suas implicações. "
                "O estudante compara interpretações, identifica pressupostos, reconhece registro e desenvolve uma resposta própria. "
                "A meta é compreender e produzir português com autonomia, precisão e flexibilidade.")


def comprensao_para(titulo):
    return [
        Ejercicio(f"Qual é o tema principal do texto sobre '{titulo}'?", f"O desenvolvimento da comunicação relacionada a {titulo}."),
        Ejercicio("O texto recomenda apenas memorizar palavras?", "Não. Recomenda compreender, praticar e usar o conteúdo em contexto."),
        Ejercicio("Qual é a meta geral do estudante?", "Usar português com autonomia progressiva.")
    ]


def exercicios_para(n, vocab):
    p1, t1 = vocab[0]
    p2, t2 = vocab[1]
    p3, t3 = vocab[2]
    return [
        Ejercicio(f"Traduza para o espanhol: {p1}", t1),
        Ejercicio(f"Traduza para o português: {t2}", p2),
        Ejercicio(f"Escreva uma frase em português usando '{p3}'.", f"Resposta livre. Exemplo: Eu uso '{p3}' em uma frase."),
        Ejercicio("Complete: Eu ____ português todos os dias. (estudar)", "estudo"),
        Ejercicio("Transforme em pergunta: Você fala português.", "Você fala português?")
    ]


def avaliacao_para(n, vocab, gramatica):
    p1, t1 = vocab[0]
    p4, t4 = vocab[3]
    return [
        Ejercicio(f"O que significa '{p1}' em espanhol?", t1),
        Ejercicio(f"Como se diz '{t4}' em português?", p4),
        Ejercicio("Escreva duas frases relacionadas ao tema do capítulo.", "Resposta livre; devem ser compreensíveis e usar o conteúdo da unidade."),
        Ejercicio("Explique com suas palavras uma regra gramatical da unidade.", gramatica[0]),
        Ejercicio("Produza oralmente uma resposta de 30–60 segundos sobre o tema.", "Autoavaliação: clareza, vocabulário, gramática e fluidez.")
    ]


def pratica_oral_para(n, titulo, vocab):
    p = [x[0] for x in vocab[:4]]
    if n <= 20:
        return [
            f"Diga em voz alta quatro frases usando: {', '.join(p)}.",
            f"Fale por 30 segundos sobre '{titulo}'.",
            "Leia o diálogo duas vezes: primeiro devagar e depois em ritmo natural."
        ]
    elif n <= 40:
        return [
            f"Fale por 1 minuto sobre '{titulo}' sem ler.",
            f"Use pelo menos quatro palavras: {', '.join(p)}.",
            "Grave-se e verifique se suas frases estão conectadas por marcadores."
        ]
    else:
        return [
            f"Faça uma exposição de 2 minutos sobre '{titulo}'.",
            f"Use de forma natural: {', '.join(p)}.",
            "Apresente uma posição, uma ressalva e uma conclusão."
        ]


def erros_para(n):
    base = [
        "Evite pronunciar todas as palavras exatamente como em espanhol.",
        "A nasalização é importante em palavras com ã, õ e ditongos nasais.",
        "Não traduza automaticamente expressões palavra por palavra."
    ]
    if n <= 20:
        base.append("Lembre-se: gostar exige normalmente a preposição de.")
    elif n <= 40:
        base.append("Cuidado ao escolher entre pretérito perfeito, imperfeito e subjuntivo.")
    else:
        base.append("Em níveis avançados, o maior risco é usar vocabulário correto em registro inadequado.")
    return base


def situacao_para(n, titulo):
    if n <= 10:
        return f"Imagine que você encontra um brasileiro. Inicie uma conversa curta relacionada a '{titulo}' e mantenha pelo menos quatro turnos."
    elif n <= 30:
        return f"Você precisa resolver uma situação real relacionada a '{titulo}'. Explique o contexto, faça uma pergunta e responda a uma possível dificuldade."
    elif n <= 50:
        return f"Participe de uma conversa ou reunião sobre '{titulo}'. Apresente seu ponto de vista, responda a uma objeção e conclua."
    return f"Prepare uma intervenção avançada sobre '{titulo}', considerando contexto, registro, possíveis ambiguidades e uma conclusão bem fundamentada."


def repaso_para(vocab, gramatica):
    return [
        "Revise todas as palavras novas sem olhar a tradução.",
        f"Explique esta regra com um exemplo próprio: {gramatica[0]}",
        f"Use em frases cinco palavras da unidade: {', '.join([x[0] for x in vocab[:5]])}.",
        "Refaça os exercícios que errou até conseguir 80% ou mais."
    ]


def construir_curso():
    capitulos = []
    for numero, nivel, titulo, objetivo in TEMAS:
        vocab = VOCAB[numero]
        gram = GRAMATICA[numero]
        cap = Capitulo(
            numero=numero,
            nivel=nivel,
            titulo=titulo,
            objetivo=objetivo,
            vocabulario=vocab,
            pronunciacion=pronunciacion_para(vocab),
            gramatica=gram,
            ejemplos=ejemplos_para(numero, vocab),
            dialogo=dialogo_para(numero, titulo, vocab),
            lectura=leitura_para(numero, titulo, vocab),
            comprension=comprensao_para(titulo),
            ejercicios=exercicios_para(numero, vocab),
            practica_oral=pratica_oral_para(numero, titulo, vocab),
            situacion_real=situacao_para(numero, titulo),
            errores_hispanohablantes=erros_para(numero),
            repaso=repaso_para(vocab, gram),
            evaluacion=avaliacao_para(numero, vocab, gram)
        )
        capitulos.append(cap)
    return capitulos


CURSO = construir_curso()


# ============================================================
# UTILIDADES DE PRESENTACIÓN
# ============================================================

def linea():
    print("=" * 76)


def mostrar_indice():
    linea()
    print("PORTUGUÊS DO BRASIL — CURSO COMPLETO A0–C1")
    linea()
    nivel_actual = None
    for c in CURSO:
        if c.nivel != nivel_actual:
            nivel_actual = c.nivel
            print(f"\nNÍVEL {nivel_actual}")
            print("-" * 40)
        print(f"{c.numero:02d}. {c.titulo}")


def obtener_capitulo(numero):
    for c in CURSO:
        if c.numero == numero:
            return c
    return None


def mostrar_capitulo(numero, mostrar_respuestas=False):
    c = obtener_capitulo(numero)
    if not c:
        print("Capítulo no encontrado.")
        return

    linea()
    print(f"NÍVEL {c.nivel} | CAPÍTULO {c.numero:02d}")
    print(c.titulo.upper())
    linea()
    print("\nOBJETIVO")
    print(c.objetivo)

    print("\n1. VOCABULÁRIO")
    for i, (pt, es) in enumerate(c.vocabulario, 1):
        print(f"{i:>2}. {pt:<24} = {es}")

    print("\n2. PRONÚNCIA ORIENTATIVA")
    for pt, pron in c.pronunciacion:
        print(f"- {pt}: {pron}")

    print("\n3. GRAMÁTICA")
    for i, g in enumerate(c.gramatica, 1):
        print(f"{i}. {g}")

    print("\n4. EXEMPLOS")
    for i, (pt, es) in enumerate(c.ejemplos, 1):
        print(f"{i}. PT: {pt}")
        print(f"   ES: {es}")

    print("\n5. DIÁLOGO")
    for falante, fala in c.dialogo:
        print(f"{falante}: {fala}")

    print("\n6. LEITURA")
    print(c.lectura)

    print("\n7. COMPREENSÃO")
    for i, e in enumerate(c.comprension, 1):
        print(f"{i}. {e.pregunta}")
        if mostrar_respuestas:
            print(f"   ✓ {e.respuesta}")

    print("\n8. EXERCÍCIOS")
    for i, e in enumerate(c.ejercicios, 1):
        print(f"{i}. {e.pregunta}")
        if mostrar_respuestas:
            print(f"   ✓ {e.respuesta}")

    print("\n9. PRÁTICA ORAL")
    for i, p in enumerate(c.practica_oral, 1):
        print(f"{i}. {p}")

    print("\n10. SITUAÇÃO REAL")
    print(c.situacion_real)

    print("\n11. CUIDADO PARA HISPANOFALANTES")
    for i, e in enumerate(c.errores_hispanohablantes, 1):
        print(f"{i}. {e}")

    print("\n12. REVISÃO")
    for i, r in enumerate(c.repaso, 1):
        print(f"{i}. {r}")

    print("\n13. AVALIAÇÃO")
    for i, e in enumerate(c.evaluacion, 1):
        print(f"{i}. {e.pregunta}")
        if mostrar_respuestas:
            print(f"   ✓ {e.respuesta}")


# ============================================================
# PROGRESO
# ============================================================

RUTA_PROGRESO = Path("progresso_portugues.json")


def cargar_progreso():
    if RUTA_PROGRESO.exists():
        try:
            return json.loads(RUTA_PROGRESO.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"completados": [], "notas": {}}


def guardar_progreso(datos):
    RUTA_PROGRESO.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def marcar_completado(numero):
    datos = cargar_progreso()
    if numero not in datos["completados"]:
        datos["completados"].append(numero)
        datos["completados"].sort()
    guardar_progreso(datos)
    print(f"Capítulo {numero} marcado como completado.")


def registrar_nota(numero, nota):
    if not 0 <= nota <= 100:
        print("La nota debe estar entre 0 y 100.")
        return
    datos = cargar_progreso()
    datos["notas"][str(numero)] = nota
    guardar_progreso(datos)
    print(f"Nota registrada: {nota}/100")


def ver_progreso():
    datos = cargar_progreso()
    completados = datos["completados"]
    porcentaje = len(completados) / len(CURSO) * 100
    linea()
    print("PROGRESO DEL CURSO")
    linea()
    print(f"Capítulos completados: {len(completados)}/{len(CURSO)}")
    print(f"Progreso general: {porcentaje:.1f}%")
    if completados:
        print("Completados:", ", ".join(map(str, completados)))
    if datos["notas"]:
        notas = [float(v) for v in datos["notas"].values()]
        print(f"Promedio de evaluaciones registradas: {sum(notas)/len(notas):.1f}/100")


# ============================================================
# MODO ESTUDIO
# ============================================================

def estudiar_capitulo(numero):
    c = obtener_capitulo(numero)
    if not c:
        print("Capítulo no encontrado.")
        return

    mostrar_capitulo(numero, mostrar_respuestas=False)
    input("\nPresiona ENTER cuando hayas terminado de estudiar...")

    print("\n--- RESPUESTAS DE COMPREENSIÓN ---")
    for i, e in enumerate(c.comprension, 1):
        print(f"{i}. {e.respuesta}")

    print("\n--- RESPUESTAS DE EJERCICIOS ---")
    for i, e in enumerate(c.ejercicios, 1):
        print(f"{i}. {e.respuesta}")

    print("\n--- GUÍA DE EVALUACIÓN ---")
    for i, e in enumerate(c.evaluacion, 1):
        print(f"{i}. {e.respuesta}")

    resp = input("\n¿Marcar este capítulo como completado? (s/n): ").strip().lower()
    if resp == "s":
        marcar_completado(numero)

    try:
        nota_txt = input("Nota de autoevaluación 0-100 (ENTER para omitir): ").strip()
        if nota_txt:
            registrar_nota(numero, float(nota_txt))
    except ValueError:
        print("Nota omitida.")


# ============================================================
# BÚSQUEDA
# ============================================================

def buscar(texto):
    texto = texto.lower().strip()
    resultados = []
    for c in CURSO:
        campos = [
            c.titulo,
            c.objetivo,
            c.lectura,
            " ".join(pt for pt, _ in c.vocabulario),
            " ".join(c.gramatica)
        ]
        if any(texto in campo.lower() for campo in campos):
            resultados.append(c)
    if not resultados:
        print("No se encontraron resultados.")
        return
    for c in resultados:
        print(f"{c.numero:02d} | {c.nivel} | {c.titulo}")



# ============================================================
# VALIDACIÓN DE INTEGRIDAD DEL CURSO
# ============================================================

def validar_curso():
    campos = [
        "numero", "nivel", "titulo", "objetivo", "vocabulario",
        "pronunciacion", "gramatica", "ejemplos", "dialogo",
        "lectura", "comprension", "ejercicios", "practica_oral",
        "situacion_real", "errores_hispanohablantes", "repaso",
        "evaluacion"
    ]
    errores = []

    if len(CURSO) != 60:
        errores.append(f"Se esperaban 60 capítulos y hay {len(CURSO)}.")

    if [c.numero for c in CURSO] != list(range(1, 61)):
        errores.append("La numeración no es consecutiva del 1 al 60.")

    for c in CURSO:
        for campo in campos:
            if not hasattr(c, campo):
                errores.append(f"Capítulo {getattr(c, 'numero', '?')}: falta '{campo}'.")
            elif getattr(c, campo) is None:
                errores.append(f"Capítulo {c.numero}: '{campo}' es None.")

        for campo in [
            "vocabulario", "pronunciacion", "gramatica", "ejemplos",
            "dialogo", "comprension", "ejercicios", "practica_oral",
            "errores_hispanohablantes", "repaso", "evaluacion"
        ]:
            if hasattr(c, campo) and not getattr(c, campo):
                errores.append(f"Capítulo {c.numero}: '{campo}' está vacío.")

        if hasattr(c, "lectura") and not str(c.lectura).strip():
            errores.append(f"Capítulo {c.numero}: lectura vacía.")
        if hasattr(c, "situacion_real") and not str(c.situacion_real).strip():
            errores.append(f"Capítulo {c.numero}: situación real vacía.")

    if errores:
        print("\nERRORES DE INTEGRIDAD:")
        for error in errores:
            print("-", error)
        return False
    return True


# ============================================================
# MENÚ
# ============================================================

def menu():
    while True:
        print("\n")
        linea()
        print("PORTUGUÊS DO BRASIL — A0 a C1")
        linea()
        print("1. Ver índice completo")
        print("2. Estudiar un capítulo")
        print("3. Ver capítulo con respuestas")
        print("4. Buscar tema o palabra")
        print("5. Ver progreso")
        print("6. Marcar capítulo como completado")
        print("7. Registrar nota")
        print("0. Salir")

        op = input("\nOpción: ").strip()

        if op == "1":
            mostrar_indice()

        elif op == "2":
            try:
                estudiar_capitulo(int(input("Capítulo 1-60: ")))
            except ValueError:
                print("Número inválido.")

        elif op == "3":
            try:
                mostrar_capitulo(int(input("Capítulo 1-60: ")), mostrar_respuestas=True)
            except ValueError:
                print("Número inválido.")

        elif op == "4":
            buscar(input("Texto a buscar: "))

        elif op == "5":
            ver_progreso()

        elif op == "6":
            try:
                marcar_completado(int(input("Capítulo: ")))
            except ValueError:
                print("Número inválido.")

        elif op == "7":
            try:
                numero = int(input("Capítulo: "))
                nota = float(input("Nota 0-100: "))
                registrar_nota(numero, nota)
            except ValueError:
                print("Datos inválidos.")

        elif op == "0":
            print("\nAté logo! Continue praticando português. 🇧🇷")
            break

        else:
            print("Opción no válida.")






# ============================================================
# INTERFAZ STREAMLIT
# ============================================================

import streamlit as st

st.set_page_config(
    page_title="Português do Brasil A0–C1",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Estilos
# ----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }
    .section-card {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
    }
    .small-muted {
        opacity: 0.7;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Progreso en session_state
# ----------------------------
if "completados" not in st.session_state:
    st.session_state.completados = set()

if "notas" not in st.session_state:
    st.session_state.notas = {}

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.markdown("## 🇧🇷 Curso")
niveles = ["A0", "A1", "A2", "B1", "B2", "C1"]
nivel_sel = st.sidebar.selectbox("Nivel", niveles)

capitulos_nivel = [c for c in CURSO if c.nivel == nivel_sel]
opciones_cap = {
    f"{c.numero:02d} — {c.titulo}": c.numero for c in capitulos_nivel
}
cap_label = st.sidebar.selectbox("Capítulo", list(opciones_cap.keys()))
cap_num = opciones_cap[cap_label]
cap = obtener_capitulo(cap_num)

st.sidebar.markdown("---")

total = len(CURSO)
hechos = len(st.session_state.completados)
st.sidebar.progress(hechos / total if total else 0)
st.sidebar.caption(f"Progreso general: {hechos}/{total} capítulos")

if cap_num in st.session_state.completados:
    st.sidebar.success("✓ Capítulo completado")
else:
    if st.sidebar.button("Marcar como completado", use_container_width=True):
        st.session_state.completados.add(cap_num)
        st.rerun()

if cap_num in st.session_state.completados:
    if st.sidebar.button("Desmarcar capítulo", use_container_width=True):
        st.session_state.completados.discard(cap_num)
        st.rerun()

# ----------------------------
# Encabezado
# ----------------------------
st.markdown('<div class="main-title">Português do Brasil</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Curso completo para hispanohablantes · A0 → C1</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"Nível {cap.nivel} · Capítulo {cap.numero:02d}")
    st.title(cap.titulo)
with col2:
    if cap_num in st.session_state.notas:
        st.metric("Última nota", f"{st.session_state.notas[cap_num]:.0f}/100")

st.info(f"🎯 **Objetivo:** {cap.objetivo}")

# ----------------------------
# Pestañas principales
# ----------------------------
tabs = st.tabs([
    "📚 Vocabulario",
    "🔊 Pronunciación",
    "📖 Gramática",
    "💬 Diálogo",
    "📘 Lectura",
    "✏️ Ejercicios",
    "🎤 Práctica oral",
    "🧠 Evaluación"
])

# VOCABULARIO
with tabs[0]:
    st.subheader("Vocabulario")
    for i, (pt, es) in enumerate(cap.vocabulario, 1):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{i}. {pt}**")
        with c2:
            st.write(es)

# PRONUNCIACIÓN
with tabs[1]:
    st.subheader("Pronunciación orientativa")
    st.caption("Guía aproximada pensada para hispanohablantes.")
    for pt, pron in cap.pronunciacion:
        st.markdown(f"- **{pt}** → `{pron}`")

# GRAMÁTICA
with tabs[2]:
    st.subheader("Gramática")
    for i, regla in enumerate(cap.gramatica, 1):
        st.markdown(f"**{i}.** {regla}")

    st.markdown("### Ejemplos")
    for i, (pt, es) in enumerate(cap.ejemplos, 1):
        with st.container(border=True):
            st.markdown(f"**PT:** {pt}")
            st.caption(f"ES: {es}")

# DIÁLOGO
with tabs[3]:
    st.subheader("Diálogo")
    for hablante, frase in cap.dialogo:
        st.markdown(f"**{hablante}:** {frase}")

    st.markdown("### Situación real")
    st.info(cap.situacion_real)

# LECTURA
with tabs[4]:
    st.subheader("Lectura")
    st.write(cap.lectura)

    st.markdown("### Comprensión")
    for i, e in enumerate(cap.comprension, 1):
        with st.expander(f"{i}. {e.pregunta}"):
            st.write(f"**Respuesta:** {e.respuesta}")

# EJERCICIOS
with tabs[5]:
    st.subheader("Ejercicios")
    st.caption("Intenta responder antes de abrir la solución.")
    for i, e in enumerate(cap.ejercicios, 1):
        with st.expander(f"{i}. {e.pregunta}"):
            st.write(f"**Solución / guía:** {e.respuesta}")

    st.markdown("### Cuidado para hispanohablantes")
    for e in cap.errores_hispanohablantes:
        st.warning(e)

    st.markdown("### Repaso")
    for i, r in enumerate(cap.repaso, 1):
        st.markdown(f"{i}. {r}")

# PRÁCTICA ORAL
with tabs[6]:
    st.subheader("Práctica oral")
    for i, p in enumerate(cap.practica_oral, 1):
        st.markdown(f"**{i}.** {p}")

    st.markdown("### Autoevaluación rápida")
    claridad = st.slider("Claridad", 0, 10, 5)
    vocab = st.slider("Vocabulario", 0, 10, 5)
    gramat = st.slider("Gramática", 0, 10, 5)
    fluidez = st.slider("Fluidez", 0, 10, 5)
    promedio = (claridad + vocab + gramat + fluidez) / 4
    st.metric("Promedio oral", f"{promedio:.1f}/10")

# EVALUACIÓN
with tabs[7]:
    st.subheader("Evaluación")
    st.caption("Responde primero por tu cuenta y luego revisa la guía.")

    puntaje = 0
    for i, e in enumerate(cap.evaluacion, 1):
        st.markdown(f"**{i}. {e.pregunta}**")
        respuesta_usuario = st.text_area(
            f"Tu respuesta {i}",
            key=f"eval_{cap.numero}_{i}"
        )
        with st.expander("Ver guía de respuesta"):
            st.write(e.respuesta)

    nota = st.slider("Registra tu nota del capítulo", 0, 100, 80)
    if st.button("Guardar nota", type="primary"):
        st.session_state.notas[cap_num] = nota
        st.success(f"Nota guardada: {nota}/100")

# ----------------------------
# Pie
# ----------------------------
st.markdown("---")
st.caption(
    "Material original de estudio. La interfaz guarda el progreso durante la sesión actual de Streamlit."
)
