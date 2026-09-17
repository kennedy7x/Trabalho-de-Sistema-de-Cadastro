# pdf_exporter.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os


class PDFExporter:
    """Classe responsável por exportar dados para PDF"""
    
    @staticmethod
    def exportar_pessoas(pessoas, caminho_arquivo=None, filtro_aplicado=None):
        """
        Exporta a lista de pessoas para um arquivo PDF
        
        Args:
            pessoas: Lista de tuplas com os dados das pessoas
            caminho_arquivo: Caminho onde salvar o PDF (opcional)
            filtro_aplicado: Termo de filtro aplicado (opcional)
        
        Returns:
            tuple: (sucesso: bool, mensagem: str, caminho: str)
        """
        try:
            # Gera nome do arquivo se não fornecido
            if not caminho_arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                caminho_arquivo = f"relatorio_pessoas_{timestamp}.pdf"
            
            # Cria o documento
            doc = SimpleDocTemplate(
                caminho_arquivo,
                pagesize=landscape(A4),
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm,
                title="Relatório de Pessoas Cadastradas",
                author="Sistema de Cadastro"
            )
            
            # Estilos
            styles = getSampleStyleSheet()
            
            titulo_style = ParagraphStyle(
                'TituloCustom',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#2C3E50'),
                alignment=TA_CENTER,
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            
            subtitulo_style = ParagraphStyle(
                'SubtituloCustom',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#7F8C8D'),
                alignment=TA_CENTER,
                spaceAfter=20
            )
            
            info_style = ParagraphStyle(
                'InfoStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#34495E'),
                alignment=TA_LEFT,
                spaceAfter=10
            )
            
            # Elementos do PDF
            elementos = []
            
            # Título
            titulo = Paragraph("📋 Relatório de Pessoas Cadastradas", titulo_style)
            elementos.append(titulo)
            
            # Subtítulo com data
            data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            subtitulo = Paragraph(
                f"Sistema de Cadastro de Pessoas | Gerado em: {data_geracao}",
                subtitulo_style
            )
            elementos.append(subtitulo)
            
            # Informações do relatório
            info_texto = f"<b>Total de registros:</b> {len(pessoas)}"
            if filtro_aplicado:
                info_texto += f" | <b>Filtro aplicado:</b> '{filtro_aplicado}'"
            
            info = Paragraph(info_texto, info_style)
            elementos.append(info)
            
            elementos.append(Spacer(1, 0.3*cm))
            
            # Cabeçalhos da tabela
            cabecalhos = [
                'ID', 'Nome', 'CPF/CNPJ', 'E-mail', 
                'Celular', 'Cidade/UF', 'Tipo', 'Data Cadastro'
            ]
            
            # Prepara os dados
            dados_tabela = [cabecalhos]
            
            for pessoa in pessoas:
                # pessoa = (id, nome, cpf_cnpj, email, celular, cep, 
                #           logradouro, numero, complemento, bairro, 
                #           cidade, estado, tipo_pessoa, data_cadastro)
                
                # Formata CPF/CNPJ
                cpf_cnpj = pessoa[2] if pessoa[2] else ""
                if len(cpf_cnpj) == 11:
                    cpf_cnpj = f"{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}"
                elif len(cpf_cnpj) == 14:
                    cpf_cnpj = f"{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}"
                
                # Formata celular
                celular = pessoa[4] if pessoa[4] else ""
                if len(celular) == 11:
                    celular = f"({celular[:2]}) {celular[2:7]}-{celular[7:]}"
                elif len(celular) == 10:
                    celular = f"({celular[:2]}) {celular[2:6]}-{celular[6:]}"
                
                # Cidade/UF
                cidade_uf = f"{pessoa[10]}/{pessoa[11]}" if pessoa[10] else ""
                
                # Tipo pessoa
                tipo = pessoa[12] if len(pessoa) > 12 else ""
                
                # Data cadastro
                data_cad = ""
                if len(pessoa) > 13 and pessoa[13]:
                    data_str = str(pessoa[13])
                    if len(data_str) >= 10:
                        data_cad = data_str[:10]
                
                # Nome (trunca se muito longo)
                nome = pessoa[1] if pessoa[1] else ""
                if len(nome) > 30:
                    nome = nome[:27] + "..."
                
                # Email (trunca se muito longo)
                email = pessoa[3] if pessoa[3] else ""
                if len(email) > 25:
                    email = email[:22] + "..."
                
                linha = [
                    str(pessoa[0]),
                    nome,
                    cpf_cnpj,
                    email,
                    celular,
                    cidade_uf,
                    tipo,
                    data_cad
                ]
                dados_tabela.append(linha)
            
            # Larguras das colunas (em cm)
            larguras = [1.2*cm, 5.5*cm, 3.5*cm, 4.5*cm, 3.2*cm, 3.5*cm, 1.8*cm, 2.5*cm]
            
            # Cria a tabela
            tabela = Table(dados_tabela, colWidths=larguras, repeatRows=1)
            
            # Estilo da tabela
            estilo_tabela = TableStyle([
                # Cabeçalho
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                
                # Corpo
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ID centralizado
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Nome à esquerda
                ('ALIGN', (2, 1), (5, -1), 'CENTER'),   # CPF, email, celular, cidade
                ('ALIGN', (6, 1), (6, -1), 'CENTER'),   # Tipo
                ('ALIGN', (7, 1), (7, -1), 'CENTER'),   # Data
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DCE4EC')),
                
                # Linhas alternadas
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
                 [colors.white, colors.HexColor('#F8FBFF')]),
                
                # Borda externa
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2C3E50')),
            ])
            
            tabela.setStyle(estilo_tabela)
            elementos.append(tabela)
            
            # Rodapé
            elementos.append(Spacer(1, 0.5*cm))
            rodape_style = ParagraphStyle(
                'RodapeStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#95A5A6'),
                alignment=TA_CENTER
            )
            rodape = Paragraph(
                "Sistema de Cadastro de Pessoas - Relatório gerado automaticamente",
                rodape_style
            )
            elementos.append(rodape)
            
            # Gera o PDF
            doc.build(elementos)
            
            return True, f"PDF exportado com sucesso!\n\nArquivo: {caminho_arquivo}", caminho_arquivo
            
        except Exception as e:
            return False, f"Erro ao exportar PDF: {str(e)}", None
    
    @staticmethod
    def exportar_pessoa_individual(pessoa, caminho_arquivo=None):
        """
        Exporta os dados de uma única pessoa para PDF (ficha cadastral)
        
        Args:
            pessoa: Tupla com os dados da pessoa
            caminho_arquivo: Caminho onde salvar o PDF (opcional)
        
        Returns:
            tuple: (sucesso: bool, mensagem: str, caminho: str)
        """
        try:
            if not caminho_arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_limpo = ''.join(c for c in pessoa[1] if c.isalnum() or c == ' ')[:20]
                caminho_arquivo = f"ficha_{nome_limpo}_{timestamp}.pdf"
            
            doc = SimpleDocTemplate(
                caminho_arquivo,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm,
                title=f"Ficha Cadastral - {pessoa[1]}",
                author="Sistema de Cadastro"
            )
            
            styles = getSampleStyleSheet()
            
            titulo_style = ParagraphStyle(
                'TituloFicha',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#2C3E50'),
                alignment=TA_CENTER,
                spaceAfter=20,
                fontName='Helvetica-Bold'
            )
            
            secao_style = ParagraphStyle(
                'SecaoStyle',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#5B9BD5'),
                spaceBefore=15,
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            
            elementos = []
            
            # Título
            elementos.append(Paragraph("📋 Ficha Cadastral", titulo_style))
            
            # Formata CPF/CNPJ
            cpf_cnpj = pessoa[2] if pessoa[2] else ""
            if len(cpf_cnpj) == 11:
                cpf_cnpj = f"{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}"
            elif len(cpf_cnpj) == 14:
                cpf_cnpj = f"{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}"
            
            # Formata celular
            celular = pessoa[4] if pessoa[4] else ""
            if len(celular) == 11:
                celular = f"({celular[:2]}) {celular[2:7]}-{celular[7:]}"
            elif len(celular) == 10:
                celular = f"({celular[:2]}) {celular[2:6]}-{celular[6:]}"
            
            # Formata CEP
            cep = pessoa[5] if pessoa[5] else ""
            if len(cep) == 8:
                cep = f"{cep[:5]}-{cep[5:]}"
            
            # Dados Pessoais
            elementos.append(Paragraph("👤 Dados Pessoais", secao_style))
            
            dados_pessoais = [
                ["Nome Completo:", pessoa[1] or ""],
                ["CPF/CNPJ:", cpf_cnpj],
                ["Tipo de Pessoa:", pessoa[12] if len(pessoa) > 12 else ""],
                ["E-mail:", pessoa[3] or ""],
                ["Celular:", celular],
            ]
            
            tabela_pessoal = Table(dados_pessoais, colWidths=[4*cm, 12*cm])
            tabela_pessoal.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#34495E')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#E8EEF2')),
            ]))
            elementos.append(tabela_pessoal)
            
            # Endereço
            elementos.append(Paragraph("📍 Endereço", secao_style))
            
            endereco_completo = f"{pessoa[6] or ''}, {pessoa[7] or ''}"
            if pessoa[8]:
                endereco_completo += f" - {pessoa[8]}"
            
            dados_endereco = [
                ["CEP:", cep],
                ["Logradouro:", pessoa[6] or ""],
                ["Número:", pessoa[7] or ""],
                ["Complemento:", pessoa[8] or "-"],
                ["Bairro:", pessoa[9] or ""],
                ["Cidade:", pessoa[10] or ""],
                ["Estado:", pessoa[11] or ""],
                ["Endereço Completo:", endereco_completo],
            ]
            
            tabela_endereco = Table(dados_endereco, colWidths=[4*cm, 12*cm])
            tabela_endereco.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#34495E')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#E8EEF2')),
            ]))
            elementos.append(tabela_endereco)
            
            # Rodapé
            elementos.append(Spacer(1, 1*cm))
            data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            rodape_style = ParagraphStyle(
                'RodapeStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#95A5A6'),
                alignment=TA_CENTER
            )
            elementos.append(Paragraph(
                f"Ficha gerada em {data_geracao} - Sistema de Cadastro de Pessoas",
                rodape_style
            ))
            
            doc.build(elementos)
            
            return True, f"Ficha exportada com sucesso!\n\nArquivo: {caminho_arquivo}", caminho_arquivo
            
        except Exception as e:
            return False, f"Erro ao exportar ficha: {str(e)}", None