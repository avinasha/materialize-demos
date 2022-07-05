module Mutations
  class CrashAntenna < GraphQL::Schema::Mutation
    # TODO: define return fields
    # field :post, Types::PostType, null: false

    # TODO: define arguments
    # argument :name, String, required: true

    # TODO: define resolve method
    # def resolve(name:)
    #   { post: ... }
    # end

    argument :antenna_id, String, required: true

    field :antenna_id, String, null: false

    def resolve(antenna_id:)
      mdb = {
	      :host=>"localhost",
	      :port=>6875,
	      :user=>"materialize",
	      :password=>"materialize",
	      :dbname=>"materialize"
      }

      conn = PG.connect(mdb)
      query = "INSERT INTO antennas_performance (antenna_id, clients_connected, performance, updated_at) VALUES (
        #{antenna_id},
        #{(rand() * 100).ceil},
        -100,
        now()
      );"

      conn.exec(query);

      { antenna_id: antenna_id }
    end
  end
end
