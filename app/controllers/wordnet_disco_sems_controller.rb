class WordnetDiscoSemsController < ApplicationController
  before_action :set_wordnet_disco_sem, only: [:show, :edit, :update, :destroy]

  # GET /wordnet_disco_sems
  # GET /wordnet_disco_sems.json
  def index
    @wordnet_disco_sems = WordnetDiscoSem.all
  end

  # GET /wordnet_disco_sems/1
  # GET /wordnet_disco_sems/1.json
  def show
  end

  # GET /wordnet_disco_sems/new
  def new
    @wordnet_disco_sem = WordnetDiscoSem.new
  end

  # GET /wordnet_disco_sems/1/edit
  def edit
  end

  # POST /wordnet_disco_sems
  # POST /wordnet_disco_sems.json
  def create
    @wordnet_disco_sem = WordnetDiscoSem.new(wordnet_disco_sem_params)

    respond_to do |format|
      if @wordnet_disco_sem.save
        format.html { redirect_to @wordnet_disco_sem, notice: 'Wordnet disco sem was successfully created.' }
        format.json { render :show, status: :created, location: @wordnet_disco_sem }
      else
        format.html { render :new }
        format.json { render json: @wordnet_disco_sem.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /wordnet_disco_sems/1
  # PATCH/PUT /wordnet_disco_sems/1.json
  def update
    respond_to do |format|
      if @wordnet_disco_sem.update(wordnet_disco_sem_params)
        format.html { redirect_to @wordnet_disco_sem, notice: 'Wordnet disco sem was successfully updated.' }
        format.json { render :show, status: :ok, location: @wordnet_disco_sem }
      else
        format.html { render :edit }
        format.json { render json: @wordnet_disco_sem.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /wordnet_disco_sems/1
  # DELETE /wordnet_disco_sems/1.json
  def destroy
    @wordnet_disco_sem.destroy
    respond_to do |format|
      format.html { redirect_to wordnet_disco_sems_url, notice: 'Wordnet disco sem was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_wordnet_disco_sem
      @wordnet_disco_sem = WordnetDiscoSem.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def wordnet_disco_sem_params
      params.require(:wordnet_disco_sem).permit(:textb1, :textb2, :disco_result, :wordnet_result, :tfidf)
    end
end
