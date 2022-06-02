
DROP TABLE IF EXISTS quantidade_funcionario;
create table quantidade_funcionario (
	id_quantidade int PRIMARY KEY,
	quantidade VARCHAR
	);


DROP TABLE IF EXISTS tipo_contratacao;
create table tipo_contratacao (
	id_tipo int PRIMARY KEY,
	tipo VARCHAR
	);


DROP TABLE IF EXISTS modelo_trabalho;
create table modelo_trabalho (
	id_modelo int PRIMARY KEY,
	modelo VARCHAR
	);


DROP TABLE IF EXISTS nivel_cargo;
create table nivel_cargo (
	id_nivel int PRIMARY KEY,
	nivel VARCHAR
	);


DROP TABLE IF EXISTS atividade;
create table atividade (
	id_atividade INT PRIMARY KEY,
	atividade VARCHAR
	);

DROP TABLE IF EXISTS vagas;
create table vagas (
	id_vaga INT PRIMARY KEY,
	titulo VARCHAR(150),
	candidatos INT,
	recrutador VARCHAR(200),
	descricao TEXT,
	empresa VARCHAR(150),
	local VARCHAR,
	aberta INT,
	data_publicacao DATE,
	servico VARCHAR,
	selo_competencia INT,
	recrutando_agora INT,
	correspondente INT,
	conexao_ensino INT,
	conexoes INT,
	tipo_contratacao INT,
	FOREIGN KEY (tipo_contratacao)
		REFERENCES tipo_contratacao(id_tipo),
	local_trabalho INT not null,
	FOREIGN KEY (local_trabalho)
		REFERENCES modelo_trabalho(id_modelo),
	nivel_cargo INT not null,
	FOREIGN KEY (nivel_cargo)
		REFERENCES nivel_cargo(id_nivel),
	quantidade_funcionario INT,
	FOREIGN KEY (quantidade_funcionario)
		REFERENCES quantidade_funcionario(id_quantidade)
	);

DROP TABLE IF EXISTS atividade_vaga;
create table atividade_vaga (
	data DATE,
	id_vaga INT,
	FOREIGN KEY (id_vaga)
		REFERENCES vagas(id_vaga),
	id_atividade int,
	FOREIGN KEY (id_atividade)
		REFERENCES atividade(id_atividade),	
	PRIMARY KEY (id_vaga, id_atividade)


	);
	
	