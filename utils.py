def modo_a_prompt(estilo):
    estilos = {
        "Normal": "",
        "Formal": "Responde de manera formal y profesional. "
                    "Usa oraciones completas, un tono respetuoso y evita jerga o expresiones informales. "
                    "No agregues comentarios personales; mantén la respuesta clara y estructurada.",
        "Modo profesor": "Explícalo como un profesor experto, paso por paso y con ejemplos.",
        "Chistoso": "Añade humor y un tono divertido a la explicación.",
        "Poético": "Responde con un tono poético y metáforas.",
    }
    return estilos.get(estilo, "")
