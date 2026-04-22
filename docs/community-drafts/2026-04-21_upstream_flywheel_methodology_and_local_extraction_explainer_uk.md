# Пояснювальна записка: upstream Flywheel methodology, локальна схема формалізації та extraction із `PLFM_RADAR`

**Дата:** 2026-04-21  
**Статус:** робоче пояснення; не офіційна upstream-дефініція  
**Аудиторія:** учасники спільноти, включно з людьми без щоденної практики програмування  
**Пов'язані артефакти:**  
- `.local/workflow/extractions/2026-04-21_flywheel_compatible_external_contributor_pr_loop_extraction_draft.md`  
- `.local/workflow/aeris10-workflow-pipeline.md`  
- `.local/memory/maintainer-patterns.md`  
- `.local/memory/upstream/2026-04-21.md`

> **Примітка про приватні посилання.** Посилання з префіксом `/Users/sd/projects/PLFM_RADAR/.local/` і `/Users/sd/.codex/` вказують на приватний corpus, який не опубліковано у цьому репо. Load-bearing content відтворено inline у тексті документа.

## Навіщо потрібен цей документ

У попередній розмові ми намагалися зрозуміти не тільки те, як працює наш локальний workflow для `PLFM_RADAR`, а й те, чи можна з нього витягти щось ширше; тобто матеріал, придатний для рівня методології.

Проблема в тому, що слова `методологія`, `workflow`, `process`, `stack`, `tools` часто змішуються. Через це одна людина під "методологією" розуміє набір інструментів, інша, порядок кроків, а третя, загальні принципи. У цій записці ми фіксуємо робоче розуміння, до якого дійшли в розмові, і робимо це в детальній формі, зрозумілій не лише програмістам.

## Три рівні, які ми розрізняємо

Далі в тексті ми тримаємо чітку межу між трьома різними речами:

1. **upstream Flywheel methodology** — описана в документації `agentic_coding_flywheel_setup`;
2. **локальна аналітична лінза** — структурна мова `kernel / operators / validators / Track A/B/C`, яку ми беремо з локального skill `operationalizing-expertise`;
3. **локальний extraction із `PLFM_RADAR`** — конкретна чернетка, що витягує evergreen частину з нашого локального workflow.

Ми не маємо одного перевіреного upstream-файлу, який був би єдиним канонічним маніфестом методології; навіть найсильніші upstream Flywheel-документи самі позначають себе як synthesized artifacts (див. provenance-цитату нижче). Тому цей документ не проголошує канон; він пояснює:

- що є upstream джерелом;
- що є нашою локальною схемою опису;
- що саме ми реально витягуємо з `PLFM_RADAR`;
- і де наш поточний матеріал уже сильний, а де він ще лише чернетковий.

## Походження і першоджерела

### A. Upstream методологічні джерела

Найближчі перевірені upstream-джерела, які справді описують методологію, це:

- [THE_FLYWHEEL_CORE_LOOP.md](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_CORE_LOOP.md#L1)
  - прямо називає себе `a beginner-friendly version of the Flywheel methodology`;
  - розводить `planning substrate` і `core operating loop`.
- `THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md` — містить чотири окремі структурні розділи, кожен зі своїм line anchor:
  - [`FLYWHEEL_KERNEL`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2053)
  - [`Operator Library`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2067)
  - [`Validation Gates`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2271)
  - [`Anti-Patterns`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2284)
- [Provenance note в цьому ж Flywheel-документі](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2894)
  - прямо показує, що цей текст уже є synthesized artifact, а не одиноким маніфестом.

Коротко, словами самого документа:

> Synthesized from ~75+ substantive X posts ... documentation, and real-world usage patterns ...

Це важлива provenance-підказка: навіть сильний upstream Flywheel document є узагальненням кількох джерел, а не єдиним "першотекстом".

### B. Локальна схема формалізації

Коли ми в розмові почали вживати структурні слова на кшталт:

- `triangulated kernel`;
- `operator library`;
- `validators`;
- `Track A / B / C`;

ми користувалися локальною схемою з:

- [operationalizing-expertise/SKILL.md](/Users/sd/.codex/skills/operationalizing-expertise/SKILL.md:1)

Тобто це не слід плутати з прямою мовою upstream Flywheel docs. Це наш локальний інструмент для того, щоб робити методологію більш формальною і відтворюваною.

### C. Локальне джерело extraction

Наш конкретний extraction у цій темі спирається на:

- [aeris10-workflow-pipeline.md](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:45)
- [upstream snapshot 2026-04-21](/Users/sd/projects/PLFM_RADAR/.local/memory/upstream/2026-04-21.md:1)
- [maintainer-patterns.md](/Users/sd/projects/PLFM_RADAR/.local/memory/maintainer-patterns.md:1)

## Як ми дивимось на "методологічний рівень"

Те, що нас цікавить у цій розмові, це не просто список тулів і не просто порядок кроків.

Це багатошарова система, де є:

1. стабільне ядро правил;
2. повторювані оператори, тобто типові когнітивні ходи;
3. цикли виконання, які збирають ці ходи в реальну роботу;
4. інструменти, які підтримують усе це технічно;
5. валідація, яка не дозволяє перетворити красиві слова на пусту декларацію.

Цей п'ятишаровий поділ є локальною аналітичною лінзою з `operationalizing-expertise`; upstream Flywheel docs структурують своє ядро інакше, про що нижче.

Інакше кажучи, методологічний рівень відповідає на питання:

- у що ми віримо як у правила хорошої роботи;
- які дії повторюємо знову і знову;
- як саме з цих дій збирається робочий цикл;
- як доводимо, що все це не є самообманом;
- якими інструментами це підтримуємо.

## Просте пояснення через аналогію

Для людей поза програмуванням зручно думати так.

Уявімо кухню:

- `kernel` це не рецепт і не каструля; це правила на кшталт "пробуй на смак, не довіряй здогаду" або "не подавай страву, поки не перевірив температуру";
- `operators` це прийоми на кшталт "спочатку скуштуй базу без спецій", "відділи текстуру від смаку", "не міняй три речі одночасно";
- `loop` це порядок роботи; підготував, скуштував, скоригував, перевірив, подав;
- `tools` це ножі, плита, ваги, термометр;
- `validation` це спосіб довести, що страва справді готова, а не "мені здається, що готова".

Якщо є тільки ножі, плита і каструлі, це ще не методологія.

Якщо є тільки рецепт, але немає правил перевірки якості, це теж не методологія.

Методологія починається там, де є **стабільні правила, відтворювані дії, порядок їх використання і перевірка результату**.

Цю аналогію теж слід читати як локальну лінзу опису, а не як дослівну upstream-схему.

## Важлива примітка про лінзу опису

Поділ на:

- `kernel`
- `operators`
- `loops`
- `tools`
- `validation`

у цьому документі є **локальною аналітичною лінзою** з `operationalizing-expertise`, а не повною upstream-вокабулярною рамкою.

Це важливо, бо upstream Flywheel docs мають свій власний `FLYWHEEL_KERNEL v0.1` у [THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2053), і його зміст інший. Там ядро говорить передусім про:

- `plan space` (архітектурне мислення в markdown-плані до коду);
- `plan-to-beads` translation (переклад плану в `beads` — самодостатні задачі з залежностями);
- `beads` як execution substrate (виконавчий шар, на якому працює swarm агентів);
- fungible swarm agents (взаємозамінні агенти без "привілейованих" ролей);
- coordination that survives crashes and compaction;
- feedback from session history назад у tools, skills і validators.

Цю різницю добре видно навіть із двох коротких дослівних формулювань upstream: `The markdown plan must be comprehensive before coding starts.` і `Swarm agents are fungible.`

Наш current extraction для `PLFM_RADAR` дивиться на інший зріз практики: дисципліну зовнішнього contributor PR loop. Тому наш candidate kernel не є "варіантом upstream FLYWHEEL_KERNEL"; це окремий локальний зріз, описаний через локальну формалізаційну лінзу.

## Чотири основні шари

### 1. Kernel

`Kernel` відповідає на питання: **які правила залишаються істинними майже за будь-яких умов**.

Це найглибший рівень. Він не залежить від конкретного репозиторію, конкретного maintainer'а або конкретного CLI.

Повний список current candidate axioms див. у [2026-04-21_flywheel_compatible_external_contributor_pr_loop_extraction_draft.md](./2026-04-21_flywheel_compatible_external_contributor_pr_loop_extraction_draft.md#L144). Саме extraction draft є тут основним source of truth для цього списку.

Сильна сторона kernel у тому, що його можна перенести в інший проєкт, і він залишиться впізнаваним.

### 2. Operators

`Operators` відповідають на питання: **яку конкретну розумову дію треба виконати, коли виникає типова ситуація**.

Оператор, це не загальна порада на кшталт "будь уважним". Це чіткий, повторюваний хід.

Наприклад:

- `Freeze-Artifact`  
  Якщо review уже йде, не гарячкуй і не переписуй документ на льоту; дочекайся завершення раунду і зроби одну консолідовану ревізію.

- `Assertion-Shape-Verify`  
  Якщо хтось каже "цей тест уже це ловить", читай саму форму перевірки, а не назву тесту. Так само — перш ніж публікувати власний artifact із named symbols, grep кожен такий symbol у реальному джерелі, не довіряй інферованим чи згаданим іменам.

- `No-Delta-No-Work`  
  Якщо зовнішній стан не змінився, не вигадуй нову роботу тільки для того, щоб виглядати зайнятим.

- `Trigger-Revalidate`  
  Якщо upstream merge, review feedback або scope change ламає стару картину, перевір передумови заново. Безпосередньо перед будь-якою публічною дією (post/push/merge) — обов'язково re-query стан цільового venue, щоб не поставити artifact на вже-закриту поверхню.

У нашому локальному матеріалі ці оператори вже описані у формі, близькій до методологічної:

- з визначенням;
- з тригерами;
- з failure modes;
- з prompt module;
- з source anchors.

### 3. Loops і протоколи

`Loop` відповідає на питання: **у якому порядку ці дії виконуються в реальній роботі**.

Для `PLFM_RADAR` це виглядає як:

`0 -> 1 -> 2 -> (3 <-> 4)* -> 5 -> 6`

Цю формулу краще читати так:

- спочатку йде `0`, потім `1`, потім `2`;
- далі може кілька разів повторюватися рух між `3` і `4`;
- після цього йде `5`, а потім `6`.

Позначення тут просте:

- `<->` означає рух туди-назад між двома фазами;
- `*` означає, що такий цикл може повторитися кілька разів.

Тут:

- `0` це upstream intel;
- `1` це candidate identification;
- `2` це strategy review;
- `3` це implementation draft;
- `4` це pre-ship review;
- `5` це ship;
- `6` це monitor and close.

Окремо існують:

- `fast-path` для вузьких змін;
- emergency paths для upstream merge, direct maintainer ask, rejection та late-discovered shared risk.

Це вже рівень workflow. Він дуже важливий, але сам по собі ще не дорівнює методології. Workflow без kernel часто стає бюрократією; kernel без workflow часто лишається гарною абстракцією.

### 4. Tools і stack

`Tools` відповідають на питання: **чим технічно підтримувати process**.

Тут важливо не змішувати Flywheel core з ширшим набором інструментів навколо нього.

**Upstream Flywheel core tools**, які прямо виділені в [THE_FLYWHEEL_CORE_LOOP.md](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_CORE_LOOP.md#L9) (список на :9-13), це:

- `br`;
- `bv`;
- `Agent Mail`;

Якщо говорити мовою upstream-документа, саме ці три інструменти складають [`heart of the system`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_CORE_LOOP.md#L15).

**Broader tooling**, яке часто з'являється поряд із Flywheel practice або в наших локальних розмовах, це вже інший шар:

- `cass`;
- `cm`;
- `ntm`;
- `gh`;
- `git`.

Останні два, `gh` і `git`, узагалі не є Flywheel-specific; це загальні інструменти, які часто присутні в реальній роботі.

У нашому локальному `PLFM_RADAR` циклі стек поки скромніший:

- `git` і `gh` для upstream intel та PR work;
- `codex` і `gemini` як зовнішні reviewers;
- `.local/workflow/` і `.local/memory/` як локальне сховище артефактів і пам'яті.

Важлива різниця така: **stack не дорівнює методології**.

Якщо замінити одні інструменти іншими, методологія може залишитися тією самою. Якщо ж залишити інструменти, але прибрати kernel, operators і validation, то залишиться лише набір утиліт без справжньої дисципліни.

## П'ятий рівень, без якого все розсипається: validation

Хоч вище ми говорили про чотири шари, є ще один обов'язковий елемент; **валідація**.

Вона відповідає на питання: **як ми доводимо, що метод працює як контракт, а не як красивий текст**.

Якщо сказати просто, validation означає: ми не лише описали хороший спосіб працювати, а й придумали спосіб перевірити, що не порушуємо його нишком.

У formal skill references це означає:

- marker-bounded sections;
- перевірку anchors;
- required fields для operator cards;
- quote bank;
- consistency checks;
- validation scripts.

На людській мові це означає таке:

- не досить просто написати "ось наші принципи";
- треба ще мати спосіб перевірити, що:
  - вони справді випливають із джерел;
  - вони не суперечать одне одному;
  - оператори описані однаково;
  - локальний шум не просочився у "загальне ядро".

Без цього методологія дуже швидко деградує у добре написану, але слабо перевірену оповідь.

## Ще один supporting layer: artifacts

Є ще один практичний шар, який зручно назвати окремо; це **artifacts**.

Artifacts, це самі носії роботи:

- brief;
- analysis;
- diff;
- review note;
- memory snapshot;
- candidate note.

Для `PLFM_RADAR` це особливо важливо, бо значна частина дисципліни тримається саме на тому, що робота живе не лише "в голові" і не лише "в чаті", а в зафіксованих артефактах, які можна reread, review і зіставити один з одним.

## Що ми з'ясували на матеріалі `PLFM_RADAR`

### Важливе розрізнення

Наш локальний документ:

- `.local/workflow/aeris10-workflow-pipeline.md`

це **не канонічна методологія**. Це локальний operational workflow.

Він дуже корисний. Він уже містить багато сильних речей:

- фази;
- gate criteria;
- hard rule про frozen artifact;
- fast-path;
- emergency sub-pipeline;
- memory hygiene;
- maintainer-style sanity check.

Але він лишається локальним, бо всередині нього живе багато речей, які не можна чесно підняти до рівня загального ядра:

- Jason-specific patterns;
- exact PR numbers;
- exact branch names;
- local path layout;
- repo-specific CI requirements;
- exact policy knobs, наприклад `max 3 rounds`.

Через це ми і зробили окремий артефакт:

- `.local/workflow/extractions/2026-04-21_flywheel_compatible_external_contributor_pr_loop_extraction_draft.md`

Його призначення, це витягнути з локального workflow те, що може пережити відрив від `PLFM_RADAR`.

## Таблиця: що саме ми маємо на увазі під кожним шаром

| Шар | На яке питання відповідає | Приклад з `PLFM_RADAR` | Що зламається, якщо шару нема |
|---|---|---|---|
| `Kernel` | Які правила дисципліни тут незмінні | `не мутувати artifact під review`, `не вірити coverage без читання assertion shape`, `не вигадувати новий цикл без delta` | Процес залишиться, але стане механічним і крихким |
| `Operators` | Яку дію виконувати в типовій ситуації | `Freeze-Artifact`, `Assertion-Shape-Verify`, `No-Delta-No-Work`, `Trigger-Revalidate` | Кожну ситуацію доведеться вирішувати наново вручну |
| `Loops` | У якому порядку працювати | `0 -> 1 -> 2 -> (3 <-> 4)* -> 5 -> 6`, fast-path, emergency paths | Хороші рішення з'являтимуться в неправильний момент або запізно |
| `Validation / Gates` | Як чесно зрозуміти, що етап пройдений | negative check, positive check, file:line evidence, maintainer-style sanity check | Виникне ілюзія завершеності без реальної перевірки |
| `Artifacts` | Де живе робота і що саме review'иться | strategy briefs, analysis files, diffs, review notes, memory snapshots | Все піде в чат, у голову або в тимчасові меседжі |
| `Tools` | Чим це технічно підтримується | `git`, `gh`, `codex`, `gemini`, `.local/` | Процес не зникне, але стане повільнішим і менш відтворюваним |

## Таблиця: які реальні епізоди вже щось породили

Мітки `PR #115`, `PR #120`, `E5`, `pre-bringup` — конкретні локальні артефакти `PLFM_RADAR` (pull requests у upstream repo, внутрішня audit-lane `E5`, гілка `fix/pre-bringup-audit-p0`). Їхнє призначення тут — показати, що кожен operator спирається щонайменше на один реальний епізод, а не на абстрактну тезу.

| Епізод | Що він показав | Що з нього народилось |
|---|---|---|
| Live review rounds навколо `PR #115` | Не можна безкарно правити artifact під час зовнішнього review | `Freeze-Artifact`, explicit `3 <-> 4` loop |
| `E5 audit` (внутрішня test-coverage audit-lane) | Назва тесту не дорівнює реальному coverage | `Assertion-Shape-Verify` |
| `2026-04-21 upstream snapshot` без змін | Відсутність нової інформації, це теж результат, і він вимагає no-op, а не activity theater | `No-Delta-No-Work` |
| `PR #120` як fast-path | Мала зміна може іти коротшим маршрутом, але дисципліна перевірок не зникає | `Narrow-Fast-Path` |
| Jason reversal у `PR #115` | Maintainer-local symmetry може бути важливішою за модельну чистоту | `Maintainer-Pattern-Preserve` як кандидатний operator |
| Ризик merge гілки `pre-bringup` (upstream audit-branch) під час in-flight роботи | Upstream motion може обнулити старий аналіз | `Trigger-Revalidate` і emergency path `E2` |

## Що з нашого матеріалу вже виглядає достатньо сильним для candidate kernel

На цей момент найбільш сильними кандидатами виглядають:

1. `No new motion without new delta`
2. `Review consumes frozen artifacts, not live prose`
3. `Coverage claims are hypotheses until assertion shape is read`
4. `Upstream motion invalidates stale confidence`

Ці чотири пункти вже виглядають доволі загальними. Вони не вимагають, щоб людина знала щось про radar, FPGA чи конкретного maintainer'а.

Менш певні, але все ще сильні кандидати:

5. `Small scope earns small process; shared risk earns full process`
6. `Maintainer-local patterns outrank model-local elegance`

Вони теж правдоподібні, але тут нам ще дуже допомогли б інші корпуси, аби переконатися, що це не переобучення на один проєкт.

## Що варто піднімати як operator library, але не як саме ядро

Окремі оператори вже виглядають добре:

- `Freeze-Artifact`
- `Assertion-Shape-Verify`
- `No-Delta-No-Work`
- `Narrow-Fast-Path`
- `Maintainer-Pattern-Preserve`
- `Trigger-Revalidate`

Але тут важливо розрізняти:

- `kernel axiom` говорить про глибоке правило;
- `operator` говорить про те, яку саме дію виконати.

Наприклад, правило "review consumes frozen artifacts" добре звучить як kernel axiom; а `Freeze-Artifact` добре звучить як operator.

## Що треба лишити локально і не піднімати в канон

Ось речі, які зараз мають лишитися лише local overlay для `PLFM_RADAR`:

- Jason-specific heuristics;
- спостереження про те, що `issue + evidence` інколи працює краще за `PR + evidence`;
- soft cap на кількість вузьких PR на тиждень;
- exact threshold на кшталт `<20 LOC`;
- rule про `Gemini` кожні три цикли;
- `.local/` path layout;
- repo-specific ship gates;
- конкретні branch names, PR numbers, candidate labels.

Причина проста; усе це або actor-specific, або repo-specific, або policy-specific. Такі речі цінні локально, але вони занадто дрібні або занадто контекстні для канонічного ядра.

## Чому ми не називаємо current extraction draft уже канонічною методологією

Причина не в тому, що чернетка слабка. Причина в тому, що **канонічність вимагає додаткового рівня доказу**.

На цей момент нам бракує:

1. ще хоча б двох аналогічних корпусів;
2. quote bank з стабільними anchors;
3. multi-model distillation;
4. triangulation;
5. validators.

Інакше кажучи, зараз ми маємо:

- сильний локальний workflow;
- хороший single-source extraction draft;
- набір правдоподібних candidate operators і candidate axioms.

Але ми ще не маємо повного права сказати: "це вже і є канонічний рівень методології".

## Пояснення для не-програмістів

Якщо треба сказати це зовсім просто, то формула така:

**Методологія, це не програма і не сайт. Це спосіб працювати так, щоб хороші результати виходили не випадково, а відтворювано.**

Для цього треба:

- знати, які правила не можна порушувати;
- знати, які прийоми застосовувати в типових ситуаціях;
- мати порядок роботи;
- мати спосіб перевірити результат;
- мати інструменти, які все це підтримують.

Тоді люди можуть працювати не лише "на інтуїції", а на основі конструкції, яку можна передавати далі.

## Де ми перебуваємо зараз і що далі

Поточний стан можна описати так:

- локальний `PLFM_RADAR` workflow уже достатньо зрілий, щоб бути джерелом extraction;
- extraction draft уже достатньо сильний для рівня `candidate kernel` і `candidate operator library`, але ще не для канонічного рівня;
- для реального переходу в канонічний рівень потрібні додаткові корпуси і формальна triangulation.

Наступний крок, це **не оголосити канон**, а зробити одну з двох речей:

1. або зібрати ще 2-3 аналогічні корпуси, щоб справді триангулятувати kernel;
2. або продовжити пояснювальну роботу для спільноти, щоб люди однаково розуміли різницю між:
   - методологією;
   - workflow;
   - local overlay;
   - стеком інструментів.

На практиці обидва напрямки потрібні; перший потрібен для строгості, другий, для донесення і спільного словника.

## Глосарій

### `artifact`

Зафіксований робочий матеріал; наприклад, brief, analysis, diff або review note.

### `kernel`

Найменший стабільний набір правил, без яких метод втрачає форму.

### `operator`

Повторюваний когнітивний або робочий прийом, який вмикається в певній ситуації.

### `workflow`

Порядок етапів, через які проходить робота.

### `fast-path`

Скорочений маршрут для справді вузьких змін, коли повний review ceremony був би непропорційним.

### `stack`

Набір інструментів і технічних засобів, які підтримують процес.

### `local overlay`

Локальний шар правил, звичок і евристик, які корисні в конкретному проєкті, але ще не тягнуть на загальну методологію.

### `validation`

Перевірка того, що правило, оператор або результат не є лише красивою декларацією.

### `validator`

Конкретна перевірка або скрипт, який контролює, що структура, поля та посилання в методологічних артефактах справді коректні.

### `upstream`

Оригінальний проєкт або команда, куди врешті має потрапити зміна.

### `CI`

Автоматичні перевірки, які запускаються під час інтеграції змін; наприклад, тести, лінтери або збірка.

### `maintainer`

Людина, яка приймає або відхиляє внески й фактично визначає, що вважається прийнятним для проєкту.

### `PR`

`Pull Request`; оформлена пропозиція внести зміну в репозиторій.

### `merge`

Прийняття зміни в основну історію проєкту.

### `rebase`

Технічне оновлення робочої гілки поверх новішого upstream-стану, щоб працювати не на застарілій основі.

### `coverage`

Наскільки добре тести реально перевіряють потрібну поведінку.

### `assertion shape`

Фактична форма перевірки всередині тесту; не назва тесту, а те, що він реально порівнює і в який спосіб.

### `triangulation`

Порівняння кількох незалежних розборів або джерел, щоб залишити в ядрі лише те, що повторюється не випадково.

### `evergreen`

Та частина матеріалу, яка має шанс бути корисною довго і в різних контекстах.

### `volatile`

Тимчасова або контекстна частина матеріалу; наприклад, конкретні PR, гілки, дати, локальні policy knobs.
