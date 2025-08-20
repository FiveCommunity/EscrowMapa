#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Automático de Decriptação Escrow
Primeiro carrega as chaves, depois decripta os arquivos
"""

import os
import subprocess
import sys
import requests
import json
import base64
import threading
import time
from colorama import Fore, init
from tqdm import tqdm

# Inicializar colorama para cores no terminal
init()

def banner():
    """Mostra o banner do programa"""
    os.system("cls || clear")
    print(f"{Fore.CYAN} _____ _              ____                                      _ _         {Fore.RESET}")
    print(f"{Fore.CYAN}|  ___(_)_   _____   / ___|___  _ __ ___  _ __ ___  _   _ _ __ (_) |_ _   _ {Fore.RESET}")
    print(f"{Fore.CYAN}| |_  | \\ \\ / / _ \\ | |   / _ \\| '_ ` _ \\| '_ ` _ \\| | | | '_ \\| | __| | | |{Fore.RESET}")
    print(f"{Fore.CYAN}|  _| | |\\ V /  __/ | |__| (_) | | | | | | | | | | | |_| | | | | | |_| |_| |{Fore.RESET}")
    print(f"{Fore.CYAN}|_|   |_| \\_/ \\___|  \\____\\___/|_| |_| |_|_| |_| |_|\\__,_|_| |_|_|\\__|\\__, |{Fore.RESET}")
    print(f"{Fore.CYAN}                                                                      |___/ {Fore.RESET}")
    print()
    print(f"{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════╗{Fore.RESET}")
    print(f"{Fore.MAGENTA}║                    {Fore.YELLOW}🚀 ESCROW DECRYPTOR{Fore.MAGENTA}                      ║{Fore.RESET}")
    print(f"{Fore.MAGENTA}║                   {Fore.YELLOW}Sistema Automático v2.0{Fore.MAGENTA}                   ║{Fore.RESET}")
    print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════════════╝{Fore.RESET}")
    print()

def validar_server_key(server_key):
    """Valida se a Server Key é válida e retorna os recursos disponíveis"""
    
    if not server_key.startswith("cfxk_"):
        return False, 0
    
    url = f"https://keymaster.fivem.net/api/validate/{server_key}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if "grants_token" in data:
                
                # Decodificar JWT para contar recursos
                try:
                    jwt_parts = data["grants_token"].split(".")
                    if len(jwt_parts) == 3:
                        payload = jwt_parts[1]
                        payload += "=" * (-len(payload) % 4)
                        decoded = base64.urlsafe_b64decode(payload).decode()
                        grants_data = json.loads(decoded)
                        
                        if "grants" in grants_data:
                            total_recursos = len(grants_data["grants"])
                            return True, total_recursos
                        else:
                            return False, 0
                    else:
                        return False, 0
                except Exception:
                    return False, 0
            else:
                return False, 0
        else:
            return False, 0
            
    except Exception:
        return False, 0

def carregar_chaves(server_key):
    """Carrega as chaves usando o escrow.py"""
    
    try:
        resultado = subprocess.run(
            ['python', 'escrow.py', '-s', '-k', server_key],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if resultado.returncode == 0:
            return True
        else:
            return False
            
    except Exception:
        return False

def verificar_arquivos_assets():
    """Verifica se há arquivos .fxap na pasta assets"""
    
    if not os.path.exists("assets"):
        return False, 0
    
    mapas_encontrados = []
    total_arquivos = 0
    
    # Procurar por pastas de mapas (cada pasta deve ter um .fxap)
    for item in os.listdir("assets"):
        item_path = os.path.join("assets", item)
        
        if os.path.isdir(item_path):
            # Verificar se esta pasta tem um arquivo .fxap
            fxap_path = os.path.join(item_path, ".fxap")
            if os.path.exists(fxap_path):
                mapas_encontrados.append({
                    'nome': item,
                    'caminho': item_path,
                    'fxap': fxap_path
                })
            
            # Contar arquivos nesta pasta
            for root, dirs, files in os.walk(item_path):
                total_arquivos += len(files)
        elif os.path.isfile(item_path):
            total_arquivos += 1
    
    if mapas_encontrados:
        return True, len(mapas_encontrados)
    else:
        return False, 0

def executar_decriptacao():
    """Executa o processo de decriptação para cada mapa individualmente com barra de progresso responsiva"""
    
    if not os.path.exists("assets"):
        return False
    
    # Encontrar todos os mapas com .fxap
    mapas_para_decriptar = []
    for item in os.listdir("assets"):
        item_path = os.path.join("assets", item)
        if os.path.isdir(item_path):
            fxap_path = os.path.join(item_path, ".fxap")
            if os.path.exists(fxap_path):
                mapas_para_decriptar.append({
                    'nome': item,
                    'caminho': item_path,
                    'fxap': fxap_path
                })
    
    if not mapas_para_decriptar:
        return False
    
    total_mapas = len(mapas_para_decriptar)
    sucessos = 0
    falhas = 0
    
    # Barra de progresso principal com atualizações em tempo real
    with tqdm(total=total_mapas, 
              desc="🔓 Decriptando Mapas", 
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
              ncols=80,
              colour='green') as pbar:
        
        # Processar cada mapa individualmente
        for i, mapa in enumerate(mapas_para_decriptar):
            # Atualizar descrição da barra de progresso
            pbar.set_description(f"🔓 {mapa['nome']}")
            
            try:
                # Executar decriptação para este mapa específico
                resultado = subprocess.run(
                    ['python', 'escrow.py', '-d', mapa['caminho']],
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                
                if resultado.returncode == 0:
                    sucessos += 1
                    # Mostrar sucesso na barra de progresso
                    pbar.set_postfix_str(f"✅ {mapa['nome']}", refresh=True)
                else:
                    falhas += 1
                    # Mostrar falha na barra de progresso
                    pbar.set_postfix_str(f"❌ {mapa['nome']}", refresh=True)
                    
            except Exception as e:
                falhas += 1
                pbar.set_postfix_str(f"❌ {mapa['nome']} (Erro)", refresh=True)
            
            # Atualizar barra de progresso
            pbar.update(1)
            
            # Calcular e mostrar porcentagem
            porcentagem = ((i + 1) / total_mapas) * 100
            pbar.set_postfix_str(f"{porcentagem:.1f}% | {mapa['nome']}", refresh=True)
            
            # Pequena pausa para mostrar o progresso
            time.sleep(0.1)
    
    return falhas == 0

def aplicar_watermark():
    """Aplica watermark nos arquivos decriptados"""
    
    try:
        resultado = subprocess.run(
            ['python', 'watermark.py', '-d', './out'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if resultado.returncode == 0:
            return True
        else:
            return False
            
    except Exception:
        return False

def main():
    """Função principal do sistema"""
    banner()
    
    # Sempre solicitar Server Key para validação
    print(f"{Fore.BLUE}🔑 CONFIGURAÇÃO DA SERVER KEY{Fore.RESET}")
    print(f"{Fore.BLUE}{'─' * 50}{Fore.RESET}")
    while True:
        print(f"{Fore.CYAN}💡 Dica: Você pode colar a chave usando Ctrl+V (Windows) ou Cmd+V (Mac){Fore.RESET}")
        
        # Entrada da chave com mascaramento visual
        server_key = ""
        prompt = f"{Fore.YELLOW}📝 Digite sua Server Key (cfxk_...): {Fore.RESET}"
        
        # Mostrar prompt e capturar entrada
        print(prompt, end="", flush=True)
        
        # Capturar entrada caractere por caractere para mascarar
        if os.name == 'nt':  # Windows
            import msvcrt
            while True:
                char = msvcrt.getch()
                if char == b'\r':  # Enter
                    break
                elif char == b'\x08':  # Backspace
                    if server_key:
                        server_key = server_key[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    try:
                        char_str = char.decode('utf-8')
                        if char_str.isprintable():
                            server_key += char_str
                            print('*', end='', flush=True)
                    except:
                        pass
            print()  # Nova linha
        else:  # Linux/Mac
            try:
                import termios
                import tty
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    while True:
                        char = sys.stdin.read(1)
                        if char == '\r' or char == '\n':  # Enter
                            break
                        elif char == '\x7f':  # Backspace
                            if server_key:
                                server_key = server_key[:-1]
                                print('\b \b', end='', flush=True)
                        elif char.isprintable():
                            server_key += char
                            print('*', end='', flush=True)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                print()  # Nova linha
            except ImportError:
                # Fallback para sistemas sem termios (como Windows)
                server_key = input().strip()
        
        # Limpar a linha da entrada para não mostrar a chave
        print(f"\033[A\033[K{Fore.GREEN}🔒 Chave recebida com sucesso!{Fore.RESET}")
        
        if server_key and server_key.startswith("cfxk_"):
            print(f"{Fore.CYAN}⏳ Validando Server Key...{Fore.RESET}")
            valida, _ = validar_server_key(server_key)
            if valida:
                print(f"{Fore.GREEN}✅ Server Key válida!{Fore.RESET}")
                print(f"{Fore.CYAN}📥 Carregando chaves no cache...{Fore.RESET}")
                if not carregar_chaves(server_key):
                    print(f"{Fore.RED}❌ Erro ao carregar chaves{Fore.RESET}")
                    input(f"\n{Fore.YELLOW}⏸️ Pressione Enter para sair...{Fore.RESET}")
                    return
                print(f"{Fore.GREEN}✅ Chaves carregadas com sucesso!{Fore.RESET}")
                break
            else:
                print(f"{Fore.RED}❌ Server Key inválida ou sem recursos{Fore.RESET}")
                print(f"{Fore.YELLOW}💡 Verifique se a chave tem acesso aos recursos necessários{Fore.RESET}")
        else:
            print(f"{Fore.RED}❌ Formato inválido! Deve começar com 'cfxk_'{Fore.RESET}")
    
    print()
    
    # Verificar se há arquivos para processar
    if not os.path.exists("assets"):
        print(f"{Fore.RED}❌ Pasta 'assets' não encontrada{Fore.RESET}")
        input(f"\n{Fore.YELLOW}⏸️ Pressione Enter para sair...{Fore.RESET}")
        return
        
    arquivos_ok, num_mapas = verificar_arquivos_assets()
    if not arquivos_ok:
        print(f"{Fore.RED}❌ Nenhum arquivo .fxap encontrado{Fore.RESET}")
        input(f"\n{Fore.YELLOW}⏸️ Pressione Enter para sair...{Fore.RESET}")
        return
    
    # Executar todo o processo - a barra de progresso aparece imediatamente aqui
    executar_decriptacao()
    aplicar_watermark()
    
    print()
    print(f"{Fore.GREEN}✅ Descriptografia finalizada com sucesso!{Fore.RESET}")
    print()
    
    # Manter o programa aberto
    print(f"{Fore.BLUE}{'=' * 60}{Fore.RESET}")
    print(f"{Fore.GREEN}🏁 Processo concluído! O programa permanecerá aberto.{Fore.RESET}")
    print(f"{Fore.YELLOW}💡 Você pode executar novamente ou fechar manualmente.{Fore.RESET}")
    print(f"{Fore.BLUE}{'=' * 60}{Fore.RESET}")
    
    while True:
        try:
            escolha = input(f"\n{Fore.CYAN}🔄 Pressione Enter para executar novamente ou 'sair' para encerrar: {Fore.RESET}").strip().lower()
            if escolha == 'sair':
                print(f"\n{Fore.YELLOW}👋 Encerrando programa...{Fore.RESET}")
                break
            elif escolha == '':
                print(f"\n{Fore.BLUE}{'='*60}{Fore.RESET}")
                print(f"{Fore.GREEN}🔄 REINICIANDO SISTEMA...{Fore.RESET}")
                print(f"{Fore.BLUE}{'='*60}{Fore.RESET}\n")
                # Limpar variáveis e reiniciar
                os.system("cls || clear")
                main()  # Reinicia o programa
                break  # Evita recursão
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}👋 Encerrando programa...{Fore.RESET}")
            break

if __name__ == "__main__":
    try:
        main()
    except:
        pass