# Transcendence makefile | Website 

#Some colors
RED = \033[0;31m
GREEN = \033[0;32m
NC = \033[0m

#Compiler

start:
	@echo "${GREEN}Starting Transcendence...${NC}"
	@docker-compose up -d --build
	@echo "${GREEN}Transcendence is running on http://localhost:8080${NC}"
	@echo "${GREEN}Initiating Vault script...${NC}"
	@bash ./configuration/vault/vault_init.sh
	@echo "${GREEN}Vault is running on http://localhost:8200${NC}"
	@echo "${GREEN}Transcendence is ready!${NC}"

clean:
	@echo "${RED}Stopping Transcendence...${NC}"
	@docker-compose down -v --rmi all --remove-orphans
	@echo "${RED}Transcendence is stopped!${NC}"

fclean: clean
	@echo "${RED}Removing all images...${NC}"
	@docker system prune -a -f
	@echo "${RED}All images are removed!${NC}"

re: fclean start

.PHONY: start clean fclean re