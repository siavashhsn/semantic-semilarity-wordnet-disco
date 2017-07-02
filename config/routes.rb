Rails.application.routes.draw do
	get 'wordnet_disco_sems/new'
	resources :wordnet_disco_sems
	root 'wordnet_disco_sems#new'
  	# For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
