# Master Dynamic Variables in Flux1
## Stop Writing Prompts by Hand

**Author:** Sergio Valsecchi  
**Date:** 22 luglio 2025

---

## Chapter 1 – Introduction: What Prompt Variables Are in Flux1

In the world of generative AI, the power of an image doesn't just come from the model or the node—it comes from how precisely the prompt is constructed. With Flux1—especially through the Kontext and T5XXL modules—you can go far beyond simple text descriptions. You can build structured prompts using dynamic variables, controlled randomness, priority weights, and modular syntax.

This guide is designed for those who want to automate and personalize image generation, fully leveraging Flux1 variables to produce high-quality, varied, and stylistically coherent content—while preserving subject identity, pose, lighting, and visual consistency.

### What You'll Learn in This Guide

Over 4 chapters, you'll discover how to:

- Write prompts using `{}` variables, combining alternative options dynamically
- Use `|`, `[ ]`, and `::` to control styling, expressions, lighting, and environments
- Install and configure the right Custom Nodes in ComfyUI to unlock these features in Flux1
- Optimize your workflow with a custom GPT, able to auto-generate prompt structures with consistency and logic

### Why Use Variables?

Prompt variables allow you to:

- Increase variety without rewriting your structure
- Control randomness with fine-tuned precision
- Generate coherent image series with targeted variations (e.g., outfit, expression, lighting)
- Save time by using reusable prompt frameworks
- Integrate GPT as a smart prompt generator for scaled production

### 🧪 A Concrete Example

**Classic prompt:**
```
She is styled in a red Versace dress under golden hour light
```

**Flux1 prompt with variables:**
```
She is styled in a {red Versace dress::1.3|black tech jumpsuit|ceramic exosuit} under {golden hour|neon-lit|foggy} light
```

With one prompt, you can generate dozens of variations, each consistent in composition but uniquely styled—perfect for fashion, automotive, product photography, or character consistency.

### Who This Guide Is For

- Creatives using ComfyUI with Flux1
- Designers and art directors who need consistent, controlled outputs
- AI professionals seeking advanced prompt automation
- Prompt engineers working with GPTs for scalable content production

---

## Chapter 2 – Variable Types and Advanced Syntax in Flux1 Prompts

### 1. Random Variables `{...}`

**Syntax:** `{option1|option2|option3}`

This is the basic randomization form. Flux1 will randomly select one of the listed options during generation.

**Example:**
```
She is wearing a {red dress|black suit|white jumpsuit}
```

### 2. Weighted Variables `{...::n}`

**Syntax:** `{option1::1.5|option2::0.7|option3}`

Assigns a "weight" to each option, controlling how likely it is to be chosen.

**Example:**
```
The outfit is a {silk robe::1.4|leather jacket::0.6|cotton shirt}
```

Here, silk robe is more likely to appear than the other options.

### 3. Optional Groups `[...]`

**Syntax:** `[element1|element2]`

Flux1 may include or skip the entire block. Use this to add optional stylistic details.

**Example:**
```
She walks through a neon-lit street[ with rain reflections| with fog]
```

### 4. Nested and Combined Variables

You can combine and nest variables to build complex yet flexible structures.

**Example:**
```
She wears a {futuristic|{retro|vintage}-inspired} {jumpsuit|bodysuit}
```

### 5. Full Example

```
She is styled in a {Versace suit::1.2|Nike techwear|ceramic armor} under {golden hour|neon-lit|overcast} light, showing a {confident smile|neutral expression|piercing gaze}[ with accessories].
```

This single prompt can generate dozens of controlled variations, all consistent in structure and framing.

### 🎯 Best Practices

- Limit each block to 4–6 options to avoid semantic confusion
- Use `::` to prioritize the options you want to appear more often
- Keep a consistent structure across prompts (same number of blocks, clean grammar)
- Write prompts in clear, direct English (avoid complex subordinate clauses)

### Extra Variables

#### 6. Multi-selection `$$`

**Syntax:** `{2$$optionA|optionB|optionC}` - Selects two different values from the group.

**Example:**
```
Wearing {2$$silver earrings|red gloves|tech visor}
```

#### 7. Range Selection `x–y$$`

**Syntax:** `{1-3$$optionA|optionB|optionC|optionD}` - Selects between x and y options randomly.

#### 8. Nested Variables

Variables can be nested for more complexity.

**Example:**
```
Wearing a {futuristic|{retro|vintage}-inspired} {jumpsuit|bodysuit}
```

#### 9. Wildcards from External Files

Pull options from external `.txt`, `.yaml`, or `.json` files.

**Example:**
```
Wearing {1-2$$__tops__|__dresses__}
```

#### 10. Combinatorial Generation

Instead of random generation, use all possible combinations of variables to create full prompt sets (great for dataset expansion or testing).

#### 11. Angled Brackets `<...>`

Alternative to `{}` syntax for key tokens (used for specific token focus or parsing in some engines).

### Example – Full Advanced Prompt

```
She is styled in {1-2$$__tops__|__jackets__} with a {silk scarf::1.4|leather strap} [with metallic accents], under {golden hour|neon-lit|foggy} lighting, showing a {neutral|confident|piercing} gaze.
```

This single line can generate hundreds of controlled variations while preserving pose, identity, and overall composition.

---

## Chapter 3 – Custom Nodes for Dynamic Prompts in Flux1 with ComfyUI

To fully unlock the power of advanced syntax and variables covered in Chapter 2, you need to install the Dynamic Prompts custom node for ComfyUI. This node allows you to use `{}` structures, weights, optional blocks, wildcards, and even combinatorial generation inside your image pipelines.

This chapter will walk you through installation, available features, and practical usage inside Flux1 workflows.

### 1. How to Install the Dynamic Prompts Node

**If you're using ComfyUI Manager:**

1. Open ComfyUI and click on Manager
2. Open Custom Nodes Manager
3. Search for "dynamicprompts" and click Install
4. Restart ComfyUI after installation

**Alternatively, install manually via terminal:**

```bash
cd your/comfyui/custom_nodes
git clone https://github.com/adieyal/comfyui-dynamicprompts
pip install -r comfyui-dynamicprompts/requirements.txt
python comfyui-dynamicprompts/install.py
mkdir comfyui-dynamicprompts/wildcards
```

Then restart ComfyUI.

### 🔍 2. Key Nodes Included

Once installed, you'll find a new section called Dynamic Prompts, which includes:

- **Random Prompts** – supports `{}`, `::`, `[]`, `$$`, and nested syntax
- **Combinatorial Prompts** – generates all possible combinations instead of picking one at random
- **I'm Feeling Lucky** – generates random prompt ideas
- **Magic Prompt** – enhances your input using a neural network for richer descriptions
- **Jinja2 Templates** – supports advanced, programmable prompt structures

### 🔄 3. Basic Workflow Setup

Here's how to integrate Dynamic Prompts into your workflow:

```
┌─────────────────────────┐
│ Random/Combinatorial    │ ← write your advanced prompt
└───────┬─────────────────┘
        │ string out
┌───────▼─────────────────┐
│     Clip Text Encode    │
└─────────────────────────┘
```

1. Use Random Prompts for dynamic randomization
2. Use Combinatorial Prompts for full coverage of all combinations
3. Optionally pass the output through Magic Prompt or Lucky
4. Then encode it with Clip Text Encoder as usual

### 4. Configuration Tips

- Store your wildcard files (`.txt`, `.yaml`, `.json`) inside the `wildcards/` folder. For example:
  - `__expressions__.txt` might include facial expressions like smile, neutral, surprised
- Enable autorefresh if you want new prompts on each execution
- ComfyUI doesn't log your final generated prompt by default — use nodes like Write Text File or AddMetaData if you need to store the result for reference

### 5. Quick Example – Random Prompt with Wildcards

1. Add the Random Prompts node to your workflow
2. Enter this prompt:
   ```
   She is styled in {1-2$$__tops__|__jackets__} under {golden hour|neon-lit} light
   ```
3. Connect the string output to Clip Text Encode
4. Optionally add Magic Prompt or I'm Feeling Lucky
5. Run your pipeline — each generation will output a unique variation

---

## Chapter 4 – Optimizing Prompt Generation with a Custom GPT

Once you've mastered variable syntax and installed the required nodes, the next step is to automate the creation of prompts. You can do this by integrating your own custom GPT trained to write Flux1-compatible prompts, based on either a reference image or a written brief.

### Two Advanced Generation Modes

#### 1. From Image (image-to-prompt)

Do you have a reference photo and want to replicate its visual style?

Ask your custom GPT to generate a prompt that:
- Preserves the composition, lighting scheme, and background
- Reproduces the outfit style with 20–40 similar variants (e.g., "Gucci total looks")
- Uses variable syntax such as `{}`, `::`, `[]`, `$$` for automated variation
- Describes the setting (e.g., "studio in Milan", "city street at sunset")
- Always includes the LoRA tag, e.g., miazelu01

**Example request:**
> Use this photo and create a prompt with 40 different Gucci outfits. Detail the style, colors, set (studio, city, etc.), and lighting. Keep the model's facial consistency from the reference.

**Example GPT output:**
```
A full-body editorial fashion portrait of miazelu01 wearing {a red silk Gucci gown|a beige monogrammed trench coat|a black leather jumpsuit|...}, styled in a {studio with softbox lighting|urban Milan street at dusk|loft with natural window light}, maintaining direct eye contact, neutral expression and symmetrical composition. The lighting is {Rembrandt|backlit|diffused daylight}.
```

#### 2. From Brief (text-to-prompt)

Only have a written concept? Your GPT can:
- Turn the idea into a detailed Flux1-style prompt
- Use Flux1 variables to control outfit, setting, lights, poses, accessories
- Integrate the identity of the AI talent (e.g., miazelu01)
- Modularize the prompt into Look, Light, Scene, Expression, Pose

**Example brief:**
> I want a fashion photo of Mia Zelu in a sporty Adidas look, shot at night in a city with neon lights and a strong runway pose.

**Example generated prompt:**
```
miazelu01 in a {blue Adidas tech tracksuit|silver reflective windbreaker|black mesh panel bodysuit}, walking confidently in a {neon-lit urban alley|modern Tokyo street|downtown Milan runway}, with a {strong gaze|neutral look|dynamic walking pose}, under {colored neon backlight|cool ambient tones}.
```

### Example: "Prompt Designer for Mia Zelu" GPT

You can build your own GPT like this: "Prompt Designer for Mia Zelu"

**What it does:**
- Interprets a brief or image
- Knows Flux1 best practices (pose, light, outfit, variable syntax)
- Automatically includes the LoRA miazelu01
- Produces prompts ready to use in Flux1 T5XXL or Flux1 editing pipelines

**Download Mia Zelu's LoRA:**
https://huggingface.co/sergio75/MiaZelu/resolve/main/miazelu01_ep12_rp20_step1000_bf16.safetensors

### 🛠️ How to Streamline the Pipeline

1. Use a pre-trained GPT aligned with Flux1 prompt structure
2. Input image or written brief → receive structured multi-variable prompt
3. Paste the prompt into the Random Prompts node in ComfyUI
4. Generate consistent variations with identity and composition locked

---

## Chapter 5 – Complete Example of a Structured Dynamic Prompt with Flux1

After exploring syntax, custom nodes, and GPT integration, this chapter provides a real-world example of a fully dynamic, Flux1-ready prompt.

The subject is miazelu01, portrayed in a futuristic fashion editorial setting as a biomechanical android. The prompt is structured in dynamic blocks to support:
- Custom GPT generation
- Automation via Random or Combinatorial Prompts
- Scalable workflows for datasets or campaigns

### Dynamic Prompt: Android Editorial – Mia Zelu

```
A futuristic full-body editorial portrait of miazelu01, reimagined as a hybrid android – half humanoid, half robotic – standing {upright|in a contrapposto stance|balanced on one leg} and centered in a {bright white studio|circular chrome chamber|holographic light cube} with {soft frontal lighting|directional rim light|diffused ambient glow}. Her face remains unmistakably hers: symmetrical and photogenic, with an oval shape and smooth, porcelain-like skin, featuring {faint freckles|a glassy cheekbone highlight|subtle gold dust texture}. Her eyes are almond-shaped, ice-blue and expressive, enhanced with a {glossy synthetic overlay|chromatic lens layer|semi-reflective irid coating} and a faint LED glow tracing the {iris|iris ring|inner pupil}. Her lips are {matte nude|chrome-pink|plasma beige}, and her short platinum-blonde curls {frame her face|fall partially across her forehead|fade into a biomech graft}, blending into a {seamless|visible|organic} {biomechanical junction|headplate interface|neural socket array} at the temples. The android transition begins just below the jawline. Her ceramic neck and torso are plated in {high-gloss white|iridescent pearl|brushed silver} armor segmented by seams glowing with {white::1.5|electric blue|soft lavender|magenta|amber} LED filaments. Visible mechanical elements include: - Arms with {brushed-metal filaments|exposed carbon rods|holographic pistons} - Spine with a glowing {core module|plasma coil|energy regulator} embedded between {the shoulder blades|vertebral fins|circuit ridges} - Hands featuring articulated {ceramic|titanium|nanopolymer} fingers with {translucent|prismatic|glass-tipped} nanoglass nails [etched with micro-symbols] Her lower body is wrapped in {white composite plating|pearlescent armor|matte poly-alloy}, revealing {soft-tech tendons|flexible fiber cables|organic-tech ligaments} that flex as she shifts weight. Legs integrate {chrome layering|soft-silicone musculature|gel-infused polymers}, with {ankle vents|micro-turbines|heat-diffusion slits} diffusing faint {blue|gold|rose} light. The entire design is {harmonious|elegant|sleek}, engineered with {post-human grace|cybernetic fashion|digital beauty} in mind. The "outfit" is {fully integrated|partially modular|sculpted} into her body – no fabric, only engineered form, as if {designed by a future fashion house|styled in a post-couture era|crafted by synthetic artisans}. Her stance is {serene and proud|cold and divine|statuesque and commanding}, enhanced by {soft light gradients|rim-backlight on ceramic|focused glow on facial planes}, resulting in a portrait that feels {emotionally distant|digitally alive|aesthetic and post-human}.
```

### Prompt Breakdown

**Block: Look & Body**
- Content: Ceramic plating, LED seams, biomechanical transitions
- Variability: LED colors, plating

**Block: Facial Details**
- Content: Eyes, freckles, lips, hair, biomech grafts
- Variability: 3–5 options per block

**Block: Environment**
- Content: Studio, chrome room, holographic light cube
- Variability: Dynamic background

**Block: Lighting**
- Content: Rim light, softbox, ambient glow
- Variability: 3 light setups

**Block: Pose**
- Content: Upright, contrapposto, single-leg stance
- Variability: Randomized

**Block: Expression**
- Content: Proud, divine, commanding
- Variability: Stylized variants

### Usage Tips

- Perfect for generating high-concept editorial AI imagery
- Useful for testing LoRA identity consistency (e.g., miazelu01) in full-body scenes
- Great for GPTs tasked with producing stylistic prompt variations automatically

---

## Chapter 6 – Fashion Prompting with Flux1: Style, Color, and Editorial Consistency

The fashion industry is one of the most fascinating—and demanding—sectors to translate into generative prompt language. It requires control, visual consistency, aesthetic sensitivity, and variety. Fortunately, Flux1 handles all of these challenges through its system of dynamic variables and subject consistency.

In this chapter, we explore how to create structured fashion photography prompts using Flux1, based on an editorial studio setup featuring Gucci outfits.

### Objective

Create a prompt that generates full-body editorial portraits featuring Gucci-inspired fashion, with controlled variation in:
- Garment style and silhouette
- Dominant outfit color
- Optional accessories
- Studio lighting conditions
- Pose and attitude

### Example – Advanced Prompt for Gucci Studio Shoot (Flux1-ready)

```
A high-fashion full-body editorial portrait of miazelu01, styled in a {tailored Gucci suit::1.3|pleated silk gown|cropped monogram two-piece|sheer tulle blouse and flare pants|structured leather jumpsuit}, featuring {vibrant red|ivory white|emerald green|royal blue|champagne gold} as dominant color, accented by {gold details|embossed textures|tone-on-tone patterns|contrasting belts}. She poses confidently in a {professional photography studio|white cyclorama space|set with colored acrylic panels|textile-draped fashion set} under {soft frontal lighting::1.5|high-key side lighting|diffused top-down light|low-angled shadows}, standing on a {glossy floor|reflective stage|matte neutral base}. Her posture is {elegant and strong|neutral and poised|fluid and dynamic|tilted and experimental}, with a {direct|soft|intense} gaze, and her body language enhances the vertical lines of the outfit. [Accessories include {oversized earrings|stacked rings|leather gloves|statement boots}, selected to complement the outfit without overshadowing it.] The styling, makeup and lighting are all designed to emphasize the texture, tailoring, and chromatic boldness of Gucci's signature fashion identity, while preserving the photorealistic traits of miazelu01 in every variation.
```

### Why It Works

This prompt uses:
- `{}` → to randomize outfits, colors, lighting, environments, poses
- `::` → to prioritize key looks (e.g., the tailored suit)
- `[]` → to insert optional accessories elegantly
- Clean and explicit editorial descriptors for studio, posture, styling

### Practical Use Cases

- AI-generated visuals for lookbooks, advertising campaigns, or concept art
- Consistency testing for a fashion character LoRA
- Rapid development of virtual outfit catalogs or editorial-style social content
- Prompt generation automation via GPT for creative teams or e-commerce platforms

---

## Chapter 7 – Fashion & Animal Symbolism: Brand Identity Through Dynamic Prompting

Fashion is more than clothing — it's identity, storytelling, and visual memory. In this final chapter, we explore how Flux1 prompts can be structured to blend fashion editorial photography with iconic animal symbols associated with luxury brands.

### Concept: Fashion meets Iconic Animal Branding

Many fashion brands use animals as symbols of their ethos:

- **Lacoste** → Crocodile = resilience, elegance
- **Kenzo** → Zebra = boldness, wild beauty
- **Roberto Cavalli** → Snake = sensuality, transformation
- **BAPE** → Ape = street intelligence, uniqueness
- **Gucci** → Tiger = strength, protection, luxury

These symbols are visual extensions of a brand's voice — and perfect elements to integrate into AI-generated fashion photography.

### Prompt Example – Gucci x Lacoste (Crocodile Motif)

```
A full-body editorial portrait of miazelu01 dressed in Gucci, paired with a Lacoste crocodile motif theme: miazelu01 wears {a tailored Gucci suit::1.3|a pleated silk Gucci gown|a structured leather Gucci jumpsuit}, featuring {emerald green|ivory white|champagne gold} as the dominant color, accented by {gold hardware|subtle monogram embossing|tone-on-tone stripes}. A stylized Lacoste crocodile motif appears as {a stitched detail on the lapel|a tonal emboss on the belt|a subtle pattern on the sleeve cuff}. She stands confidently in a {professional white studio|minimalist cyclorama set|high-fashion chrome backdrop} under {soft frontal lighting::1.5|dramatic side lighting|diffused top-down light}, on a {glossy platform|textured white floor|reflective base}. Her pose is {upright and powerful|fluid and dynamic|tilted and editorial}, with a {direct|soft|intense} gaze. Optional details: [Accessories include {oversized earrings|stacked rings|statement boots}]. The crocodile detail enhances the luxury identity, blending Gucci elegance with Lacoste heritage — symbolizing power, resilience, and timeless style.
```

### Gucci x Lacoste – The Crocodile Studio Shoot

```
A full-body editorial portrait of miazelu01 dressed in Gucci, paired with a Lacoste crocodile motif theme and accompanied by a live crocodile as part of the visual concept. miazelu01 wears {a tailored Gucci suit::1.3|a pleated silk Gucci gown|a structured leather Gucci jumpsuit}, featuring {emerald green|ivory white|champagne gold} as the dominant color, accented by {gold hardware|subtle monogram embossing|tone-on-tone stripes}. A stylized Lacoste crocodile motif appears as {a stitched detail on the lapel|a tonal emboss on the belt|a subtle pattern on the sleeve cuff}. At her side, a real crocodile rests calmly on the set — its posture controlled and majestic, symbolizing {strength and elegance|timeless luxury|brand heritage}. Its textured skin contrasts with the polished textures of the outfit, creating a deliberate visual dialogue between nature and couture. The scene is set in a {professional white studio|minimalist cyclorama set|high-fashion chrome backdrop} under {soft frontal lighting::1.5|dramatic side lighting|diffused top-down light}, with miazelu01 standing on a {glossy platform|textured white floor|reflective base}, just beside the animal. Her pose is {upright and powerful|fluid and dynamic|tilted and editorial}, with a {direct|soft|intense} gaze. Optional details: [Accessories include {oversized earrings|stacked rings|statement boots}]. The presence of the crocodile brings a layer of raw symbolism to the image — bridging the refined identity of Gucci with the athletic heritage of Lacoste. The resulting portrait is not only fashion-forward, but conceptually layered, merging luxury, instinct, and visual power.
```

---

## Final

This guide was designed to make you a master of dynamic prompting with Flux1. From syntax and custom nodes to GPT integration and fashion-specific case studies, you now have the tools to create modular, expressive, scalable prompts that deliver results — whether for concept art, brand campaigns, or AI-powered fashion production.