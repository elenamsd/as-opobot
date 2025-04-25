db.user.insertMany([
    {
        _id: 1,
        name: "User 1",
        session: 1,
        created_at: new Date(),
        oppositions: [1, 4]
    },
    {
        _id: 2,
        name: "User 2",
        session: 2,
        created_at: new Date(),
        oppositions: [2, 5]
    },
    {
        _id: 3,
        name: "User 3",
        session: 3,
        created_at: new Date(),
        oppositions: [3]
    }
]);

db.opposition.insertMany([
    {
        _id: 1,
        title: "CONVOCATORIA PARA LA COBERTURA DE 2 PLAZAS DE TÉCNICO SUPERIOR INFORMÁTICO, FUNCIONARIO/A DE CARRERA, MEDIANTE EL SISTEMA DE CONCURSO-OPOSICIÓN",
        created_at: new Date(),
        modified_at: new Date(),
        source: "Ayuntamiento La Laguna",
        start_date: new Date("2023-01-01"),
        end_date: new Date("2023-12-31"),
        category: "Matemáticas",
        status: "Cerrado",
        url: "https://www.aytolalaguna.es/ayuntamiento/empleo-publico/CONVOCATORIA-PARA-LA-COBERTURA-DE-2-PLAZAS-DE-TECNICO-SUPERIOR-INFORMATICO-FUNCIONARIO-A-DE-CARRERA-MEDIANTE-EL-SISTEMA-DE-CONCURSO-OPOSICION/"
    },
    {
        _id: 2,
        title: "CONVOCATORIA PARA LA COBERTURA DE 1 PLAZA DE ARQUITECTO/A TÉCNICO, FUNCIONARIO/A DE CARRERA, MEDIANTE EL SISTEMA DE CONCURSO-OPOSICIÓN",
        created_at: new Date(),
        modified_at: new Date(),
        source: "Ayuntamiento La Laguna",
        start_date: new Date("2023-02-01"),
        end_date: new Date("2023-11-30"),
        category: "Informática",
        status: "Cerrado",
        url: "https://www.aytolalaguna.es/ayuntamiento/empleo-publico/CONVOCATORIA-PARA-LA-COBERTURA-DE-1-PLAZA-DE-ARQUITECTO-A-TECNICO-FUNCIONARIO-A-DE-CARRERA-MEDIANTE-EL-SISTEMA-DE-CONCURSO-OPOSICION/"
    },
    {
        _id: 3,
        title: "Resolución de 24 de febrero de 2025, por la que se aprueba la convocatoria de contratación para la provisión de plazas de personal docente e investigador contratado temporal en régimen de derecho laboral, mediante procedimiento ordinario, en la figura de Profesor Asociado en Ciencias de la Salud.",
        created_at: new Date(),
        modified_at: new Date(),
        source: "Universidad de La Laguna",
        start_date: new Date("2023-03-01"),
        end_date: null,
        category: "Ciencias",
        status: "Abierto",
        url: "https://www.ull.es/portal/convocatorias/convocatoria/resolucion-de-24-de-febrero-de-2025-por-la-que-se-aprueba-la-convocatoria-de-contratacion-para-la-provision-de-plazas-de-personal-docente-e-investigador-contratado-temporal-en-regimen-de-derecho-labo/"
    }
]);
