import matplotlib.pyplot as plt
import numpy as np

def simulate_progression(max_level=20):
    levels = np.arange(1, max_level + 1)
    xp_to_next = [100]
    for i in range(1, max_level):
        xp_to_next.append(int(xp_to_next[-1] * 1.1))
    
    total_xp = np.cumsum(xp_to_next)
    
    # Atributos (Base 10, +2 por level)
    strength = 10 + (levels - 1) * 2
    agility = 10 + (levels - 1) * 2
    intelligence = 10 + (levels - 1) * 2
    
    # Status Derivados
    hp = 100 + (strength * 5)
    mp = 50 + (intelligence * 5)
    stamina = 100 + (agility * 2)
    damage = 10 + (strength // 2)
    
    # Simulação de Inimigos (Slime base: 30 HP, 10 Dano)
    # Supondo que a cada 5 levels a dificuldade do inimigo dobra
    enemy_hp = 30 * (1.2 ** (levels - 1))
    enemy_damage = 10 * (1.1 ** (levels - 1))
    
    # Métrica: Quantos hits para matar o player vs player matar inimigo
    hits_to_kill_enemy = enemy_hp / damage
    hits_to_kill_player = hp / enemy_damage
    
    # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Progressão de XP
    axs[0, 0].plot(levels, xp_to_next, label='XP p/ Próximo Nível', marker='o')
    axs[0, 0].set_title('Progressão de XP')
    axs[0, 0].set_xlabel('Nível')
    axs[0, 0].set_ylabel('XP')
    axs[0, 0].legend()
    
    # 2. Atributos e Status
    axs[0, 1].plot(levels, hp, label='HP Máx', color='red')
    axs[0, 1].plot(levels, mp, label='MP Máx', color='blue')
    axs[0, 1].plot(levels, stamina, label='Stamina Máx', color='green')
    axs[0, 1].set_title('Status do Jogador')
    axs[0, 1].set_xlabel('Nível')
    axs[0, 1].legend()
    
    # 3. Dano vs HP Inimigo
    axs[1, 0].plot(levels, damage, label='Dano Player', color='orange', marker='s')
    axs[1, 0].plot(levels, enemy_hp, label='HP Inimigo (Escalado)', color='purple', linestyle='--')
    axs[1, 0].set_title('Dano Player vs HP Inimigo')
    axs[1, 0].set_xlabel('Nível')
    axs[1, 0].legend()
    
    # 4. Equilíbrio de Combate (Time to Kill)
    axs[1, 1].plot(levels, hits_to_kill_enemy, label='Hits p/ Matar Inimigo', color='brown')
    axs[1, 1].plot(levels, hits_to_kill_player, label='Hits p/ Morrer (Player)', color='black', linestyle=':')
    axs[1, 1].set_title('Equilíbrio de Combate (TTK)')
    axs[1, 1].set_xlabel('Nível')
    axs[1, 1].set_ylabel('Quantidade de Hits')
    axs[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/dragon-evolution-rpg/docs/balance_analysis.png')
    print("✓ Simulação concluída e gráfico salvo em docs/balance_analysis.png")

if __name__ == "__main__":
    simulate_progression()
