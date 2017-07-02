class CreateWordnetDiscoSems < ActiveRecord::Migration[5.0]
  def change
    create_table :wordnet_disco_sems do |t|
      t.text :textb1
      t.text :textb2
      t.string :disco_result
      t.string :wordnet_result
      t.string :tfidf

      t.timestamps
    end
  end
end
